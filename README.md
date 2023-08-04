# Myota Cyberstorage
Myota secures unstructured data through a dynamic object storage interface that supports your cloud workloads, including applications, webpages and hyperconverged infrastructure. Our storage solution uses an Amazon S3-compatible (S3C) interface that is easy to configure and ideal for building modern applications that require scale and flexibility, as well as importing existing data for backup or archive.

Myota Cyberstorage runs as a server agent to replace your standard S3 bucket usage. Any of your current S3 workloads that support [endpoint URLs](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/index.html) are candidates to be replaced with Myota Cyberstorage. Check out our [web site](https://www.myota.io/myota-methodology/secure-data-storage-s3-buckets) for more details.

---

## How to Use Myota Cyberstorage
Typically the only change that has to be made to switch from using a standard S3 bucket to Myota Cyberstorage is to update your credentials and provide the endpoint URL of your S3C instance. Here are some examples using the Boto3 Python SDK and the AWS CLI. Other client APIs would require similar change but will vary slightly by language or product. See our [gallery demo](./samples/gallery-demo/) for a fully functioning example with S3 and S3C working side by side.

### Credentials

Your credentials can either be included as environment variables or added as part of an AWS profile. See CLI section below for command line examples. Alternatively add your credentials at ~/.aws/credentials like:

```AWS
[myota-s3c]
aws_access_key_id=MY*****
aws_secret_access_key=*******
```
Code your application using the AWS CLI or SDK (e.g. Python Boto3)

### Using AWS CLI

```Bash
$> AWS_ACCESS_KEY_ID=MY***** AWS_SECRET_ACCESS_KEY=******* aws s3api list-objects --bucket demo-a791a751 --endpoint-url YOUR_ENDPOINT_URL

 - or -

$> AWS_PROFILE=myota-s3c aws s3api list-objects --bucket demo-a791a751 --endpoint-url YOUR_ENDPOINT_URL

{
    "Contents": [
        {
            "Key": "hello-myota.txt",
            "LastModified": "2022-05-04T00:01:45.538000+00:00",
            "ETag": "\"m69009402066f8019f1349ec006cfb50\"",
            "Size": 29,
            "StorageClass": "STANDARD",
            "Owner": {
                "DisplayName": "",
                "ID": ""
            }
        }
    ]
}
```

### Using SDK

Example 1

```Python
import boto3

s3 = boto3.resource('s3', endpoint_url='YOUR_ENDPOINT_URL')
bucket = s3.Bucket('demo-a791a751')

for obj in bucket.objects.all():
    print(obj.key)
```

Example 2

```Python
import boto3

s3 = boto3.client('s3', endpoint_url='YOUR_ENDPOINT_URL')
response = s3.list_objects_v2(Bucket='demo-a791a751')

for obj in response['Contents']
    print(obj['Key'])
```

Run Python

```Bash
$> AWS_PROFILE=myota-s3c python3 your_script.py
```
