import base64
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from .models import Image
from django.conf import settings
from django.utils import timezone
import boto3
from os.path import splitext
import time
import mimetypes
import urllib.parse

boto3.set_stream_logger(name='botocore')

aws_session = boto3.session.Session(
    settings.S3_CREDENTIAL["AccessKeyId"], settings.S3_CREDENTIAL["SecretAccessKey"])
s3Conn = aws_session.client("s3")


myota_session = boto3.session.Session(
    settings.S3C_CREDENTIAL["AccessKeyId"], settings.S3C_CREDENTIAL["SecretAccessKey"])
s3CConn = myota_session.client("s3", endpoint_url=settings.S3C_ENDPOINT_URL)


def save_image(request):

    if request.method == 'POST':
        if request.user.is_authenticated:
            type = request.POST.get('type', '')
            if type not in ['s3', 's3c']:
                return HttpResponse('missing type', status=400)
            file = request.FILES.get('file', None)
            if not file:
                return HttpResponse('missing file', status=400)

            s = splitext(file.name)
            if len(s) != 2:
                return HttpResponse('invalid file name', status=400)
            ext = s[1].strip('.').lower()

            img = Image(store_type=type, pub_date=timezone.now(),
                        ext=ext, name=file.name)
            img.save()

            if type == 's3':
                upload(s3Conn, file, settings.S3_BUCKET_NAME, img.name)
            else:
                upload(s3CConn, file, settings.S3C_BUCKET_NAME, img.name)

            time.sleep(3)
            return redirect('/')
        else:
            return HttpResponse("not authenticated", status=401)
    elif request.method == 'GET':
        if request.user.is_authenticated:
            return render(request, 'save.html')
        else:
            return redirect('/admin/login/?next=/')
    else:
        return Http404


def list_image(request):
    if request.user.is_authenticated:
        type = request.GET.get('type', '')
        imgs = None

        if type:
            imgs = Image.objects.filter(
                store_type=type).order_by('-pub_date')[:8]
        else:
            imgs = Image.objects.order_by('-pub_date')[:8]

        ctx = []

        for img in imgs.all():
            bucket = settings.S3_BUCKET_NAME
            if img.store_type == 's3c':
                bucket = settings.S3C_BUCKET_NAME
            item = {
                'name': img.name,
                'uuid': img.uuid,
                'pub': img.pub_date,
                'type': img.store_type,
                'url': s3_path_address(request, bucket, img.name),
            }
            ctx.append(item)

        return render(request, 'list.html', context={'images': ctx})
    else:
        return redirect('/admin/login/?next=/')


def upload(conn, file, bucket, key):
    print('upload to', bucket, key)
    conn.upload_fileobj(file, bucket, key)


def fetch(conn, bucket, key):
    print('download from', bucket, key)
    return conn.get_object(Bucket=bucket, Key=key)

def s3_path_address(request, bucket, key):
    p = request.get_full_path()
    url = request.build_absolute_uri()
    host = url[:-len(p)]
    return "%s/%s/%s" % (host, bucket, urllib.parse.quote_plus(key, safe='/'))



def fetch_image(request, bucket, quoted_plus_key):
    resp = None
    key = urllib.parse.unquote_plus(quoted_plus_key)
    if bucket == settings.S3_BUCKET_NAME:
        resp = fetch(s3Conn, bucket, key)
    else:
        resp = fetch(s3CConn, bucket, key)
    bin = resp['Body'].read()
    mime_type, _ = mimetypes.guess_type(key)
    return HttpResponse(bin, content_type=mime_type)

