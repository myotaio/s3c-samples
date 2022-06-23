# Myota S3-Compatible Interface
Myota secures unstructured data through a dynamic object storage interface that supports your cloud workloads, including applications, webpages and hyperconverged infrastructure. Our storage solution is compatible with S3 buckets, easy to configure and ideal for building modern applications that require scale and flexibility, as well as importing existing data for backup or archive.

Myota S3C runs as a server agent to replace your standard S3 bucket usage. Any of your current S3 workloads that support [endpoint URLs](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/index.html) are candidates to be replaced with Myota S3C. Check out our [web site](https://www.myota.io/myota-methodology/secure-data-storage-s3-buckets) for more details.


## Myota Console
The Myota Console is an additional SaaS offering that makes the administration of Myota S3C and all other Myota products much easier. It is a web based portal that adds the following features:
* Support for additional non-S3 storage nodes such as Azure Blob Storage, Google Cloud Storage, MinIO and on-premise servers.
* The ability to seemless migrate between storage providers to avoid vendor lock-in with no downtime.
* Automatic storage repair should a node lose data, become corrupt or go offline for an extended period.
* Dashboards to monitor performance, storage alerts and track usage trends.
* A CLI to simply S3C configuration.
* Myota Client management to provide all of the Myota protections for your Windows, macOS and VDI devices.

[Contact Myota](https://www.myota.io/contact) to learn more about getting the Myota Console. Instructions below will specify whether they are applicable to S3C Standalone or with Console Support.


## How to Deploy Myota S3C

### AWS Marketplace
In the AWS Console navigate to the AMI Catalog under EC2 and search for "Myota S3C". This will find the latest release of the product. Once found click "Select" and "Launch instance with AMI" to provision the EC2 instance as you normally would.

The AMI provides a script under `/var/lib/myota/config/init.sh` to make the creation of the required S3 buckets and associated IAM users and roles easier. However the EC2 instance will require elevated permissions to create all of these. See [instance-iam-role.json](./aws-ami-config/instance-iam-role.json) for the permissions that will be required. Please note the `YOUR_REGION`, `YOUR_ACCOUNT` and `YOUR_SSM_PREFIX` will have to be changed to match your environment. These can be applied to your instance by clicking "Create new IAM role" under "Step 3: Configure Instance Details".

The Myota S3C utilizes the following ports. So they should be included in the security group associated with the instance.
|Port|Usage|
|---|---|
|9986|S3C API via HTTP|
|9987|S3C API via HTTPS|
|5899|S3C API via Webdav (optional)|
|22|SSH (optional after setup)|

### Other Providers
Myota S3C currently only supports AWS AMI deployments. Instructions for additional deployment scenarios such as Microsoft Azure, Google Cloud Platform, Linode and on-premise will be published soon!


## Myota Bucket Configuration

### Standalone Mode (without Console Support)
The AMI comes with an initialization script at `/var/lib/myota/config/init.sh` that can either be run interactively with user prompts for each value or in an unattended mode that is suitable as part of a [user data script](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html). The script takes the following parameters:
|Parameter|Description|
|---|---|
|appName|Application name that will be used as the bucket name|
|ssmPrefix|Prefix to apply to all SSM parameters to avoid naming collisions|
|namePrefix|Prefix to apply to all created AWS resources (IAM users, roles, S3 buckets, etc)|
|nameSuffix|Suffix to apply to all created AWS resources (IAM users, roles, S3 buckets, etc)|
|regions|Comma separated list of four regions to create buckets in. Duplicate regions are allowed but not recommended|
|createBuckets|yes/no whether script should create the storage buckets|
|unattended|flag to suppress prompts to run unattended|

Example usage:
```Bash
$> /var/lib/myota/config/init.sh --appName gallery-demo --ssmPrefix /myota/s3c --namePrefix myota-s3c --nameSuffix gallery --regions us-east-1,us-east-2,us-west-1,us-west-2 --createBuckets yes --unattended 2>&1
```
The default access key and secret will be found in the SSM Parameter Store under `$ssmPrefix/$appName/api/v1/storapp/$appName/role/config`. So for the example command above it would be under `/myota/s3c/gallery/api/v1/storapp/gallery/role/config`.

### With Console Support

```Bash
$> cd /var/lib/myota
$> ./myota-s3c-cli --server https://CONSOLE_API_ADDRESS
```

```Myota_CLI
> login YOUR_ACCESS_KEY YOUR_ACCESS_SECRET
> create-storage-app app=gallery-demo folder=/gallery-demo storage-pool='1' device-group='2'
create-storage-app result={"appName":"gallery-demo","folderName":"gallery-demo","repoURI":"tag:myota.io,2019:repo/1/f3886505-a56f-4f21-882c-XXXXXXXXXXXX","storagePoolId":"1"}

> print-var createdApps
print-var result={"gallery-demo":{"appName":"gallery-demo","credentials":{"id":"2t9mXXXXXXXXXXXXXXXXXXXXXX","secret":"1ut6XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"},"deviceId":"ee682b2d-b8fc-42ab-9f2d-XXXXXXXXXXXX","deviceKey":"ca002d87-e201-49cf-a8dc-XXXXXXXXXXXX","repoURI":"tag:myota.io,2019:repo/1/f3886505-a56f-4f21-882c-XXXXXXXXXXXX"}}

> list-storage-app-role gallery-demo
list-storage-app-role result={"applications":[{"appName":"gallery-demo","roles":[{"accessKey":"GVBDXXXXXXXXXXXXXXX","role":"Default","secret":"hWgeXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"}]}]}
```


## How to Use Myota S3C
Typically the only change that has to be made to switch from using a standard S3 bucket to Myota S3C is to update your credentials and provide the endpoint URL of your S3C instance. Here are some examples using the Boto3 Python SDK and the AWS CLI. Other client APIs would require similar change but will vary slightly by language or product. See our [gallery demo](./samples/gallery-demo/) for a fully functioning example with S3 and S3C working side by side.

### Credentials

Add your credentials at ~/.aws/credentials

```AWS
[myota-s3c]
aws_access_key_id=W1****
aws_secret_access_key=5F**
```
Code your application using AWS SDK (e.g. Python Boto3)

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

### Using AWS CLI

```Bash
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
