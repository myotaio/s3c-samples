from django.db import models
import uuid


class Image(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    store_type = models.CharField(max_length=8)
    ext = models.CharField(max_length=8)
    name = models.CharField(max_length=255)
    pub_date = models.DateTimeField('date published')
