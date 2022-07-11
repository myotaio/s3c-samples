# Myota S3-Compatible Interface
Myota secures unstructured data through a dynamic object storage interface that supports your cloud workloads, including applications, webpages and hyperconverged infrastructure. Our storage solution is compatible with S3 buckets, easy to configure and ideal for building modern applications that require scale and flexibility, as well as importing existing data for backup or archive.

Myota S3C runs as a server agent to replace your standard S3 bucket usage. Any of your current S3 workloads that support [endpoint URLs](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/index.html) are candidates to be replaced with Myota S3C. Check out our [web site](https://www.myota.io/myota-methodology/secure-data-storage-s3-buckets) for more details.


## Myota Console
The Myota Console is an additional SaaS offering that makes the administration of Myota S3C and all other Myota products much easier. It is a web based portal that adds the following features:
* Support for additional non-S3 storage nodes such as Azure Blob Storage, Google Cloud Storage, MinIO and on-premise servers.
* The ability to seemless migrate between storage providers to avoid vendor lock-in with no downtime.
* Automatic storage repair should a node lose data, become corrupt or go offline for an extended period.
* Dashboards to monitor performance, storage alerts and track usage trends.
* A command-line interface (CLI) to simplify remote S3C configuration.
* Myota Client management to provide all of the Myota protections for your Windows, macOS and VDI devices.

[Contact Myota](https://www.myota.io/contact) to learn more about getting the Myota Console. Instructions below are only applicable to S3C Standalone without Console Support.


## How to Deploy Myota S3C

### AWS Marketplace
In the AWS Console navigate to the AMI Catalog under EC2 and search for "Myota S3C". This will find the latest release of the product. Once found click "Select" and "Launch instance with AMI" to provision the EC2 instance as you normally would.

The AMI provides a script under `/var/lib/myota/config/init.sh` to make the creation of the required S3 buckets and associated IAM users and roles easier. However the EC2 instance will require elevated permissions to create all of these. See [instance-iam-role.json](./aws-ami-config/instance-iam-role.json) for the permissions that will be required. Please note the `YOUR_REGION`, `YOUR_ACCOUNT` and `YOUR_SSM_PREFIX` will have to be changed to match your environment. These can be applied to your instance by clicking "Create new IAM profile" under "Advanced details" in the new console experience or by clicking "Create new IAM role" under "Step 3: Configure Instance Details" in the old console experience. In both cases EC2 would be the trusted service and the modified [instance-iam-role.json](./aws-ami-config/instance-iam-role.json) would be applied as its policy. See [IAM roles for Amazon EC2
](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html) for more details.

Since the init script uses the AWS CLI to create the resources, the EC2 instance requires access to the following services either by being in a public subnet or having access to a NAT gateway/instance with proper route tables.
* SSM
* KMS
* IAM
* S3

The Myota S3C utilizes the following ports. So they should be included in the security group associated with the instance. Depending on how you launch your EC2 instance these ports may be included by default.
|Port|Usage|
|---|---|
|9986|S3C API via HTTP|
|9987|S3C API via HTTPS (optional)|
|5899|S3C API via Webdav (optional)|
|22|SSH (optional after setup)|

### Other Providers
Myota S3C currently only supports AWS AMI deployments. Instructions for additional deployment scenarios such as Microsoft Azure, Google Cloud Platform, Linode and on-premise will be published soon!


## Myota Bucket Configuration

### Standalone Mode (without Console Support)
The AMI comes with an initialization script at `/var/lib/myota/config/init.sh` that can either be run interactively with user prompts for each value or in an unattended mode that is suitable as part of a [user data script](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html). The script takes the following parameters:
|Parameter|Description|
|---|---|
|appName|Application name that will be used as the **bucket name**|
|ssmPrefix|Prefix to apply to all SSM parameters to avoid naming collisions|
|namePrefix|Prefix to apply to all created AWS resources (IAM users, roles, S3 buckets, etc)|
|nameSuffix|Suffix to apply to all created AWS resources (IAM users, roles, S3 buckets, etc)|
|domains|Comma separated list of FQDNs and/or IP addresses that the service will be listening on|
|regions|Comma separated list of four regions to create buckets in. Duplicate regions are allowed but not recommended|
|createBuckets|Boolean "yes" or "no" whether script should create the storage buckets|
|unattended|Flag to suppress prompts during unattended executions|

Example usage:
```Bash
$> /var/lib/myota/config/init.sh --appName gallery-demo --ssmPrefix /myota/s3c --namePrefix myota-s3c --nameSuffix gallery --domains mys3c.myota.cloud,127.0.0.1 --regions us-east-1,us-east-2,us-west-1,us-west-2 --createBuckets yes --unattended
```

The default access key and secret will be found in the SSM Parameter Store under `$ssmPrefix/$appName/api/v1/storapp/$appName/role/config`. So for the example command above it would be under `/myota/s3c/gallery/api/v1/storapp/gallery/role/config`.


## How to Use Myota S3C
Typically the only change that has to be made to switch from using a standard S3 bucket to Myota S3C is to update your credentials and provide the endpoint URL of your S3C instance. Here are some examples using the Boto3 Python SDK and the AWS CLI. Other client APIs would require similar change but will vary slightly by language or product. See our [gallery demo](./samples/gallery-demo/) for a fully functioning example with S3 and S3C working side by side.

### Credentials

Your credentials can either be included as environment variables or added as part of an AWS profile. See CLI section below for command line examples. Alternatively add your credentials at ~/.aws/credentials like:

```AWS
[myota-s3c]
aws_access_key_id=MY*****
aws_secret_access_key=*******
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
