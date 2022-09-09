# Amazon AWS

[Prerequisites](#Prerequisites)

[Connecting](#Connecting)

[CreateRDS](#CreateRDS)

[EKSCluster](#EKSCluster)

[VPCPeering](#VPCPeering)

[S3Buckets](#S3Buckets)

[Deploy](#Deploy)

[Cronjobs](#Cronjobs)

[Traefik](#Traefik)

[Clean](#Clean)

[Troubleshooting](#Troubleshooting)

<a name="Prerequisites"></a>

## Prerequisites

First you'll have to create an Amazon AWS account in [here](https://portal.aws.amazon.com/billing/signup?nc2=h_ct&src=default&redirect_url=https%3A%2F%2Faws.amazon.com%2Fregistration-confirmation#/start). Or a digitalocean account [here](https://cloud.digitalocean.com/registrations/new)

Afterwards, create an IAM user to have access to the Amazon CLI (Command Line interface)
See here for doing that: <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html.>

Create a an acces key pair for that user and save the csv in a secure location.
It can never be accessed again, you must create a new one.

Or get an OAuth token for DOcean [here](https://cloud.digitalocean.com/settings/applications).
You can save the token in your env vars so that it is easily accesible.

`export TOKEN=your_token_here`

Then you have to install the AWS Command Line Interface `awscli`:

[Here}(<https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html>)

After that run `aws configure` and input your credentials, that are in the csv you saved.
The region we normally use is `us-east-2`, and the output format is `json`.

And also install `jq` for handling jsons:

`sudo apt install jq`

Then you have to create a key pair for your IAM user: <https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html>

Install docker securely <https://docs.docker.com/install/linux/docker-ce/ubuntu/>

And if you are in linux add your user to the docker group to be able to run it
without sudo:

```bash
sudo groupadd docker
sudo usermod -aG docker $USER
```

To use your own repository in dockerhub, you can use `docker login`. To use
amazon ECR (Elastic container repository) follow [these](https://aws.amazon.com/blogs/compute/authenticating-amazon-ecr-repositories-for-docker-cli-with-credential-helper/) instructions.

[Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) To give
order to the Kubernetes (k8) cluster from your pc.
In Linux, download the latest executable with:

```bash
curl -LO https://storage.googleapis.com/kubernetes-release/release/`curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt`/bin/linux/amd64/kubectl
```

Make the kubectl binary executable.

`chmod +x ./kubectl`

Move the binary in to your PATH.

`sudo mv ./kubectl /usr/local/bin/kubectl`

Test to ensure the version you installed is up-to-date:

`kubectl version`
We will also need eksctl. Download and extract the latest release of eksctl with the following command:

`curl --silent --location "https://github.com/weaveworks/eksctl/releases/download/latest_release/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp`

Move the extracted binary to /usr/local/bin.q

`sudo mv /tmp/eksctl /usr/local/bin`

Test that your installation was successful with the following command.

`eksctl version`

We will also need to install helm. A program to make packages of kubernetes
clusters that are parameterizable.(<https://helm.sh/docs/intro/install/)>

Beware of the version you install. As of now we are using `helm2` but `helm3`
is the latest release and cannot handle `helm2` repos.

To make sure it is installed in your cluster you must run:
`helm init`
while being in the context of your cluster for kubectl.

The postgresql client could also be useful for checking the db's.
`sudo apt-get install postgresql-client`

It is important that you are logged in your aws console. For doing this with multi-factor
you must use sts like this (First se your user and then very fast token and commands):

```bash
UNAME=<your iam username> \
TOKEN=<your mfa token> \
export STS=$(aws sts get-session-token --serial-number arn:aws:iam::906062568112:mfa/$UNAME --token-code $TOKEN) &&\
export AWS_ACCESS_KEY_ID=$(echo $STS | jq -r '.Credentials.AccessKeyId') &&\
export AWS_SECRET_ACCESS_KEY=$(echo $STS | jq -r '.Credentials.SecretAccessKey') &&\
export AWS_SESSION_TOKEN=$(echo $STS | jq -r '.Credentials.SessionToken')
```

If you have the `$AWS_PROFILE` env var set unset with `unset AWS_PROFILE`. Or else it will override your env tokens.

<a name="Connecting"></a>

## Connecting

If you only want to use kubectl for an existing cluster, you'll have to get the
user arn, like this:

`export ARN=$(aws iam get-user | jq -r '.User.Arn')`
`export USERN=<your username>`

And then someone with access to the cluster has to create this IAM mapping:

```bash
eksctl create iamidentitymapping --cluster cactus-eksctl --arn $ARN --username $USERN --group system:masters
```

However, if you want users to only be able to see the logs, create an IAM user, with only programmatic acces and no permissions.

Add this RBAC Role and rolebindings to kubernetes, (write this to a yaml file and upload it with `kubectl apply`)

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: default
  name: pod-and-pod-logs-reader
rules:
- apiGroups: [""]
  resources: ["pods", "pods/log"]
  verbs: ["get", "list"]
---
kind: RoleBinding
apiVersion: rbac.authorization.k8s.io/v1beta1
metadata:
  name: $USERN-role
  namespace: default
subjects:
- kind: User
  name: $USERN
  apiGroup: ""
roleRef:
  kind: Role
  name: pod-and-pod-logs-reader
  apiGroup: ""
```

And create the new user in the configmap:

```bash
eksctl create iamidentitymapping --cluster cactus-eksctl --arn $ARN --username $ARN --group pod-and-pod-logs-reader
```

After that you'll have to tell kubectl to use the context of the cluster
you want:
<https://docs.aws.amazon.com/eks/latest/userguide/create-kubeconfig.html>

`aws eks --region <region> update-kubeconfig --name <name of cluster>`

You can get the name in your AWS user with this command:

`aws eks list-clusters`

To get access to the Kubernetes Dashboard if it has been deployed you'd:

`kubectl proxy`

and then gain access by using the following link in your localhost:
<http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/#/login>

The new dashboard has more security and uses a bearer token to allow access.
You must choose token in the api and paste the output of this command:

`aws eks get-token --cluster-name cactus-eksctl | jq -r '.status.token'`

*If you have more than one context*, save the config file for that context in
`${HOME}/.kube` and assign those names to the `KUBECONFIG` env variable like this:
`export KUBECONFIG=${HOME}/.kube/config:${HOME}/.kube/docean-config` in your
`.zshrc`, `.yarnrc` or `.bashrc`.

You can then choose the context by listing them: `kubectl config get-contexts`
and by choosing one `kubectl config use-context <context_name>`
<a name="CreateRDS"></a>


## Create VPC
You must have a VPC for the database and one for the cluster, for more security.

To create a VPC yuo can do so in the VPC service of AWS. Be sure that your CIDR block
(that is the range of private IPs you will be able to use) doesn't intersect
with your other VPC's. I recommend having a small range because the cluster has its own inter IP's.
So using a mask of /26 for 64 IPs could be a good idea.
The awscli command for this would be:

```bash
export VPC_ID=$(aws ec2 create-vpc \
  --cidr-block 172.32.0.0/26 --amazon-provided-ipv6-cidr-block \
  --tag-specification ResourceType=vpc,Tags='[{Key="Name",Value="inguz-test-dbs"}]' \
  | jq -r '.Vpc.VpcId')
```

We save the vpc id for later use.

Then you must add 3 subnets to make use of the availability zones. You can do so in the console in the VPC service
or with a command that looks like this:

```bash
export $SUBNET_A=$(aws ec2 create-subnet \
  --vpc-id $VPC_ID \
  --availability-zone ${AWS_REGION}a \
  --cidr-block 172.32.0.0/28 \
  --tag-specification ResourceType=subnet,Tags='[{Key="Name",Value="inguz-test-dbs-a"}]' \
  | jq -r '.Subnet.SubnetId')

export $SUBNET_B=$(aws ec2 create-subnet \
  --vpc-id $VPC_ID \
  --availability-zone ${AWS_REGION}b \
  --cidr-block 172.32.0.16/28 \
  --tag-specification ResourceType=subnet,Tags='[{Key="Name",Value="inguz-test-dbs-b"}]' \
  | jq -r '.Subnet.SubnetId')

export $SUBNET_C=$(aws ec2 create-subnet \
  --vpc-id $VPC_ID \
  --availability-zone ${AWS_REGION}c \
  --cidr-block 172.32.0.32/28 \
  --tag-specification ResourceType=subnet,Tags='[{Key="Name",Value="inguz-test-dbs-c"}]' \
  | jq -r '.Subnet.SubnetId')
```

And add them to a subnet group so that you can assig it to an rds cluster. `export SUBNET_GROUP=inguz-test-dbs-abc`

```bash
aws rds create-db-subnet-group --db-subnet-group-name $SUBNET_GROUP \
  --db-subnet-group-description "For the rds database cluster" \
  --subnet-ids $SUBNET_A $SUBNET_B $SUBNET_C
```

## Create RDS Database

Now, we'll create the database using Amazon RDS, because it has these advantages
over a database created with an instance in our cluster:

* Managed high availability and redundancy.
* Ease of scaling up or down (i.e. vertical scaling) by increasing or
decreasing the computational resource for the database instance to
handle variable load.
* Ease of scaling in and out (i.e. horizontal scaling) by creating replicated
  instances to handle high read traffic.
* Automated snapshots and backups with the ability to easily roll
  back a database.
* Performing security patches, database monitoring etc.

To do this, we first need a security group, so that the DB can be accessed from
outside.
Lets create some path variables for the local session to reuse:

```bash
export AWS_REGION=us-east-2 \
export SECURITY_GROUP_NAME=inguz_test_rds_sg
```

**If you created your DB in a VPC where there is another DB that communicates
with this cluster, and you use the same security group. Then you can also skip the
VPC peering Connection section. Just make sure to save the SecurityGroup in
a var:

```bash
export SECURITY_GROUP_ID=$(aws ec2 describe-security-groups \
  --filters Name=vpc-id,Values=$VPC_ID Name=group-name,Values=$SECURITY_GROUP_NAME \
  | jq -r '.SecurityGroups[].GroupId')
```

The we create the security group. We are assuming you create the database in the
default VPC:

```bash
aws ec2 create-security-group \
--description ${SECURITY_GROUP_NAME} \
--group-name ${SECURITY_GROUP_NAME} \
--vpc-id ${VPC_ID} \
--region ${AWS_REGION}
```

We will later add the permissions after creating the EKS cluster and VPC peering connection.

Now to create the database:

```bash
export AWS_REGION=us-east-2 \
export RDS_DATABASE_NAME=inguztest \
export RDS_TEMP_USER=inguz \
export RDS_TEMP_PASS=2Wm-%pJp,M \
```

```bash
aws rds create-db-instance \
--db-instance-identifier ${RDS_DATABASE_NAME} \
--db-name ${RDS_DATABASE_NAME} \
--db-subnet-group-name ${SUBNET_GROUP} \
--vpc-security-group-ids ${SECURITY_GROUP_ID} \
--allocated-storage 20 \
--db-instance-class db.t3.small \
--engine postgres \
--master-username ${RDS_TEMP_USER} \
--master-user-password ${RDS_TEMP_PASS} \
--region ${AWS_REGION} \
--multi-az \
--backup-retention-period 1 \
--no-publicly-accessible
```

It is importante to use this `${RDS_DATABASE_NAME}` in your cleandatabase script for production. Which in our case is
`drop_db.py`.

Remember that you can scale up the database later so no need to create a big one if you dont have mucho data yet.

If you have aws KMS encryption enabled, I recommend uploading the user and passwords as generic secrets with this kind of command:
`kubectl create secret generic dev-db-secret --from-literal=username=$RDS_TEMP_USER --from-literal=password=$RDS_TEMP_PASS`

Wait for at least 7 minutes before the db finishes creating and then
run `export RDS_ADDRESS=$(aws rds describe-db-instances --profile=$PROF --filters "Name=db-instance-id,Values=$RDS_DATABASE_NAME" | jq -r ".DBInstances[].Endpoint.Address")`
to get the Endpoint address.

To access the database you can do so through a psql session, though you have to
have it installed:
You also have to add your ip to the security group you created.
DO NOT FORGET TO SET PUBLIC ACCESIBILITY TO TRUE if you want to acces from your computer!
And to check that the route table of the VPC your DB is in has an internet gateway!
`psql -h $RDS_ADDRESS -U ${RDS_TEMP_USER}`

If you want to know the IP of the instance in the psql session:
`SELECT inet_server_addr();`

To list the databases `\l`. drop_db.py has some useful commands.

To delete the DB you run:

```bash
aws rds delete-db-instance \
--skip-final-snapshot \
--db-instance-identifier ${RDS_DATABASE_NAME} \
--region ${AWS_REGION} \

```

<a name="EKSCluster"></a>

## Create the EKS cluster

`eksctl`, the framework required to work with the Amazon EKS
(Elastic Kubernetes) command line tool can be installed like this in linux:

```bash
curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp \ 
sudo mv /tmp/eksctl /usr/local/bin

eksctl version
```

*Amazon EKS is a service that charges 0.2$/cluster/hour to manage the master
node of your workers. One can also use kops to manage the master node
manually, but that also has to be hosted so the price difference isn't
very high. Even though the master node is managed by EKS, one is able to
control it as usual with kubectl, so it's not like it's a black box.*

When you create a cluster your kube context is automatically assigned
If you have other cluster be sure that yu vpc-cidr doesnt overlap with
the others:

```bash
eksctl create cluster --name=inguz-test --node-type=t2.micro --nodes=3 \
  --region=${AWS_REGION} --nodes-min 1 --nodes-max 4 --vpc-cidr 192.169.0.0/16
```

If you get this error:
AWS::EC2::EIP/NATIP: CREATE_FAILED – "The maximum number of addresses has been reached. (Service: AmazonEC2; Status Code: 400; Error Code: AddressLimitExceeded; Request ID: 4e3feabc-df46-498d-be44-27411c69754a; Proxy: null)"

Then it probably means you have reached the limit of the elastic IPs you can have. Check your limit with:

```bash
aws service-quotas get-service-quota --service-code vpc --quota-code  L-0263D0A3 --region $AWS-REGION
```

And then ask for an increase with this command:

```bash
aws service-quotas request-service-quota-increase --service-code vpc --quota-code  L-0263D0A3 --region us-east-2 --desired-value 20
```

After that you must delete the stack in the CloudFormation service in the AWS console to be able to run the create cluster command agian.

Also a Virtual Private Cloud in AWS is generated. It is best to not use an
existing vpc because this one is create with its own rules.
If you want to do so See: <https://eksctl.io/usage/vpc-networking/>

To delete the cluster you'd have to use:

```bash
eksctl delete cluster --name=cactus-eksctl
```

But yo must first delete the nodegroup that it has attached, and delete the cloudformation stack.

**If you created your DB in a VPC where there is another DB that communicates
with this cluster, and you use the same security group. You can skip the
VPC peering Connection section**

<a name="VPCPeering"></a>

## VPC peering Connection

For the DB and EKS to comunicate you'll have to create VPC peering connection:
<https://docs.aws.amazon.com/vpc/latest/peering/create-vpc-peering-connection.html>

TO do this we have to get some of the ids.

Get the VPC id of the DB in RDS, the VPC id from eks, the CIDR from EKS and CIDR from RDS DB:

```bash
export DB_VPC=$(aws rds describe-db-instances --db-instance-identifier $RDS_DATABASE_NAME  | jq -r '.DBInstances[].DBSubnetGroup.VpcId') \
export EKS_VPC=$(aws ec2 describe-vpcs --filters Name=tag:Name,Values=*cactus*  | jq -r '.Vpcs[].VpcId') \
export EKS_CIDR=$(aws ec2 describe-vpcs --filters Name=tag:Name,Values=*cactus*  | jq -r '.Vpcs[].CidrBlock') \
export DB_CIDR=$(aws ec2 describe-vpcs --vpc-ids $DB_VPC  | jq -r '.Vpcs[].CidrBlock')
```

* Go to the VPC service in AWS and then go to VPC peering connections
* Choose create vpc peering connections
  * Requester must be the VPC of the RDS database
  * Another VPC to peer with must be the VPC of EKS
  * Code:

   `export PEER_VPC=$(aws ec2 create-vpc-peering-connection --vpc-id $DB_VPC --peer-vpc-id $EKS_VPC  | jq -r '.VpcPeeringConnection.VpcPeeringConnectionId')`

* In actions choose accept connection.
  * Code:

   `aws ec2 accept-vpc-peering-connection --vpc-peering-connection-id $PEER_VPC`

* Then routing tables need to be updated for both VPCs. For the EKS routing
table (for all private subnets) a new route should be created with a destination
which corresponds to CIDR IP of RDS VPC, and the peering connection as a target.
Similarly, you need to create a new route for the RDS routing table. This step,
probably, is the most tricky one.
  * Code:

```bash
export SUBNET_EKS=$(aws ec2 describe-route-tables --filters Name=tag:Name,Values=*inguz*Public*) \
&& aws ec2 create-route --route-table-id \
$(echo $SUBNET_EKS | jq -r ".RouteTables[].RouteTableId") \
--destination-cidr-block $DB_CIDR --vpc-peering-connection-id $PEER_VPC  \
&& export SUBNET_DB=$(aws ec2 describe-route-tables --filters Name="vpc-id",Values=$DB_VPC) \
&& aws ec2 create-route --route-table-id $(echo $SUBNET_DB | jq -r ".RouteTables[].RouteTableId") \
--destination-cidr-block $EKS_CIDR --vpc-peering-connection-id $PEER_VPC
```

* We assume `eksctl` creates three private subnets and the containers may
  be in any one of them

* Update the security group to allow the CIDR's from EKS
  * Code:

```bash
aws ec2 authorize-security-group-ingress \
--group-id ${SECURITY_GROUP_ID} \
--protocol tcp \
--port 5432 \
--cidr $EKS_CIDR \
--region ${AWS_REGION} \

```

* After that enable DNS propagation for the peering connection

```bash
aws ec2 modify-vpc-peering-connection-options \
--vpc-peering-connection-id $PEER_VPC \
--requester-peering-connection-options\
 '{"AllowDnsResolutionFromRemoteVpc":true}' \
 --accepter-peering-connection-options\
  '{"AllowDnsResolutionFromRemoteVpc":true}' \
  --region $AWS_REGION 
```

<a name="Deploy"></a>

## S3 Buckets

In this part of the tutorial I will show you how to setup AWS S3 buckets
for static file handling in Django. This buckets will have the
following features:

* Private Files with automatic admin handling
  via the `PrivateMediaStorage` model Field from the `django-storages` pip package.
* Public Files via the `StaticStorage` field.
* Forced SSL connection via aws policies.
* CORS, because the static files won't be served with cross site calls (CORS) in AWS. You have to allow that specifically.
* Logs to be able to conform to security standards.

When creating the Bucket don't **enable public access**.

You must also disable **ACL ownership** in the Object Ownership section in Permissions for the bucket.

Enable **Server access logging** in the Properties tab, but be careful to do
it in **another bucket** because it will take up more space in the same bucket.
The neccesary policies will be added automatically.

Add this Policy to the bucket polices in Permissions to **force SSL**:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Allow inguz_django to read, delete and write",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::906062568112:user/inguz_django"
            },
            "Action": [
                "s3:PutObject",
                "s3:GetObjectAcl",
                "s3:GetObject",
                "s3:ListBucket",
                "s3:DeleteObject",
                "s3:PutObjectAcl"
            ],
            "Resource": [
                "arn:aws:s3:::statics-spei/*",
                "arn:aws:s3:::statics-spei"
            ]
        },
        {
            "Sid": "IPAllow",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject*",
            "Resource": [
                "arn:aws:s3:::statics-spei",
                "arn:aws:s3:::statics-spei/*"
            ]
        },
        {
            "Sid": "AllowSSLRequestsOnly",
            "Effect": "Deny",
            "Principal": "*",
            "Action": "s3:*",
            "Resource": [
                "arn:aws:s3:::statics-spei",
                "arn:aws:s3:::statics-spei/*"
            ],
            "Condition": {
                "Bool": {
                    "aws:SecureTransport": "false"
                }
            }
        }
    ]
}
```

To avoid the error of static files serving in the browser, add this CORS policy.
Bear in mind that
you must have POST and PUT to be able to upload new files. Maybe you want to omit
DELETE for more security.

```json
[
    {
        "AllowedHeaders": [
            "*"
        ],
        "AllowedMethods": [
            "GET",
            "PUT",
            "POST",
            "DELETE"
        ],
        "AllowedOrigins": [
            "https://<yourdomain>"
            "http://127.0.0.1:8000",
            "http://127.0.0.1:8001"
        ],
        "ExposeHeaders": [],
        "MaxAgeSeconds": 3000
    }
]
```

Then the Django config must look like this in `settings.py`:

```python
if(USE_S3):
    AWS_ACCESS_KEY_ID = env.str('AWS_KEY_ID', "")
    AWS_SECRET_ACCESS_KEY = env.str('AWS_SECRET_ID', "")
    AWS_S3_USE_SSL=True
    AWS_STORAGE_BUCKET_NAME = '<bucket name>'
    AWS_S3_REGION_NAME = 'us-east-2'
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    AWS_DEFAULT_ACL = None
    # s3 static settings
    AWS_LOCATION = '<static folder name>'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'
    STATICFILES_STORAGE = 'speicatalogo.storage_backends.StaticStorage'
    # s3 private media settings
    PRIVATE_MEDIA_LOCATION = 'private folder name'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PRIVATE_MEDIA_LOCATION}/'
    DEFAULT_FILE_STORAGE = 'speicatalgo.storage_backends.PrivateMediaStorage'
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
    STATIC_URL = '/static/'
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
```

The `storage_backends.py` file must look like this:

```python
from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings


class StaticStorage(S3Boto3Storage):
    location = settings.AWS_LOCATION


class PrivateMediaStorage(S3Boto3Storage):
    location = settings.PRIVATE_MEDIA_LOCATION
    file_overwrite = False
    custom_domain = False
```

And don't forget to add the urls in `urls.py`:

```python
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

## Deploy the app

We have to build the containers with their respective Dockerfiles:

```bash
docker build --rm -t paquidios/inguz:django3.7 -f docker/Dockerfile_builder . \
&& docker build --rm -t paquidios/inguz:cactus0.1 docker/Dockerfile . \
&& docker build --rm -t paquidios/inguz:sphinxdoc -f docker/Dockerfile_sphinx .
```

And then push them with `docker push paquidios/inguz:django3.7`

Or with the ECR:

```bash
docker build --rm -t 906062568112.dkr.ecr.us-east-2.amazonaws.com/cactus:django3.7 -f docker/Dockerfile_builder . \
&& docker build --rm -t 906062568112.dkr.ecr.us-east-2.amazonaws.com/cactus:cactus0.1 -f docker/Dockerfile . \
&& docker build --rm -t 906062568112.dkr.ecr.us-east-2.amazonaws.com/cactus:sphinxdoc -f docker/Dockerfile_sphinx .
```

Beware that the "." a the end of the command means that you will be using the
current directory. And you cannot copy files to your image that are not in the
dir you specifiy. If'd wanted to use files from a dir up you'd have to write
something like "../".

Then you have to push the images to the registry. Make sure to change the
helm folder to the name of the app you want to deploy. Package the file first:

```bash
helm package kubernetes/charts/cactus-stage
```

Before uploading the helm we have to upload the necessary secrets.
Where the secret.yaml file was generated via this command:

```bash
kubectl create secret docker-registry --dry-run=true docker-regcred --docker-server=https://index.docker.io/v1/ --docker-username=paquidios --docker-password=<password> --docker-email=paquidios@gmail.com -o yaml > docker-secret.yaml
```

And it is for pulling the images out of the container registry DockerHub.
By the way this would be a secure way to generate the key, not with the kind
Opaque that just uses a base64 encryption that can be cracked easily. Although with kms the 
opaque kind is automatically encrypted.
Even though it is not stored in any file that can be easily accessed.

If you have your containers in an Amazon ECR, follow this guide to create a
kubernetes cronjob that updates the secrets with the self-renewed credentials
that ECR uses:

<https://medium.com/@damitj07/how-to-configure-and-use-aws-ecr-with-kubernetes-rancher2-0-6144c626d42c>

However you must create a service account role that has the neccesary permissions:

```bash
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1beta1
metadata:
  name: ecr-secret-controller

rules:
  - apiGroups:
      - ""
    resources:
      - secrets
    verbs:
      - get
      - list
      - watch
      - create
      - delete
  - apiGroups:
      - ""
    resources:
      - serviceaccounts
    verbs:
      - get
      - list
      - watch
      - patch

---
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1beta1
metadata:
  name: ecr-secret-controller

roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: ecr-secret-controller
subjects:
  - kind: ServiceAccount
    name: ecr-secret-controller
    namespace: default

---
apiVersion: v1
kind: ServiceAccount
metadata:
  namespace: default
  name: ecr-secret-controller

---
```

Save this in a `.yaml` file and deploy it with the `kubectl apply -f <name>.yaml`
command

And you must remember to add a line around the following block of code to specify a
service account that has permissions to delete and create services. We can use
an existing one to fill that role like in the example below

```yaml
spec:
  template:
    metadata:
      creationTimestamp: null
    spec:
      serviceAccountName: ecr-secret-controller
      containers:
      - command:
        - /bin/sh
```

The other file is for the passwords of the database. It has this form:

```yaml
---
kind: Secret
apiVersion: v1
metadata:
  name: postgres-credentials
data:
  password: YnJhdHRkZXY=
  user: YnJhdHRkZXY=
type: Opaque

```

Secrets must no be saved in the git repo, so that they are not accessible. Where the pass and user
are encoded in base64, but they are passed with a newline, so its best to
encode them in this site: <https://www.base64encode.org/>

Only after having the secret and the package should you install it by giving
the address of the database, and the name of the secret:

```bash
helm upgrade cactus-site --install --force --recreate-pods cactus-0.1.0.tgz --set \
rdsExternal=kubernetes-django-east2.c4csey4k0tc5.us-east-2.rds.amazonaws.com \
--set dbSecret=postgres-credentials \
--set prodSettings=cactus.settings.prod \
--set nameOverride=cactus-site \
--set image.tag=${{ github.sha }} --set deleteDB=true --set s3.enabled=true \
--set twilio.enabled=true
```

The name override is very important to make copies of the same deployment but
with another basis name. That way you don't have to change the name of the
project every time and you can use different databases with the rdsExternal
address.

To delete it you have to copy the release name from the message you get
after installing and use it for the command. The name of the releases
is usually of the form `lazy-hydra`:
`helm delete <release name>`

The whole point of k8 is to be able to update the deployments, after making
changes to the arguments you passed to a container or to the image itself.
That's why it is useful to create a manifest with your specific values and be
able to tweak it. An example would be to get the deployment with this command:

```bash
helm template cactus-stage-0.1.0.tgz -x templates/deployment.yaml --set rdsExternal=$RDS_ADDRESS --set dbSecret=postgres-credentials-dde --set prodSettings=cactus.settings.prod --set nameOverride=catus-stage > kubernetes/deployment.yaml
```

After that you change the parameters you want and then update running:

`kubectl apply -f kubernetes/deployment.yaml`

Or take the deployment down with:

`kubectl delete -f kubernetes/deployment.yaml`

This should set you up with a running django installation. The public hostname
is handled by traefik, but you can access the pod by port forwarding to your computer.
The instructions for doing so appear after a successful installing of your chart.
This is donde with the `NOTES.txt` file that always appears after a successful
install.

<a name="Cronjobs"></a>

## Cronjobs

I have created a helm chart for deploying cronjobs based on some modifications
I made to the the manage.py script in the app. The cronjobs use a configmap to
upload a python script of your choosing and then run `python manage.py` to load
the app and run your script. You should never run any other django command with
chart because it will run the script multiple times.

Before installing the chart you have to upload a configmap with a distinct name
and giving it the file you wnat to upload, eg.:

`kubectl create configmap cronjob --from-file=kubernetes/cronjobs/cronjobs.py`

After that, you must first package the chart if you hadn't already:

`helm package kubernetes/charts/cronjob-django`

And then you cant install it by giving the name of the map. **It is very
important that you give the same nameOverride as the one you gave for the
deployment of the app you want the cronjob to work on**:

```bash
helm install cronjob-django-0.1.0.tgz --set dbSecret=postgres-credentials-dde \
--set prodSettings=dinerodeemergencia.settings.prodoction \
--set schedule='* */1 * * *' --set nameOverride=dde-test --set configMap=cronjob\
--set configPath=dinerodeemergencia/cronjob
```

Where the `configPath` must be set so that it is in a folder located where
`manage.py` is. Also the `nameOverride` has to have the name of the helm install
you did, because it uses to get the service of the DB.

The schedule gives how often the cronjob should be executed. It goes like this:

  1. Minutes
  2. Hours
  3. Days
  4. Months
  5. Weekday
If yo just give a number it will execute at that time of that field, but the
`*/1` notation means it will do it every interval of that field.

<a name="Traefik"></a>

## Ingress with Traefik

### Prerequisites

This assumes you followed the steps above. But make sure you are
connected to your kubectl context with a valid AWS IAM user (See [Connecting](#Connecting))

We will be using Traefik as an ingress controller and load balancer
to redirect all the external traffic to your apps.
Additionally, we will be using ExternalDNS to create the AWS
Rule Sets from just the services. This part is mainly
based on this two user guides:

* [Traefik & CRD & Let's Encrypt](https://docs.traefik.io/v2.0/user-guides/crd-acme/)
* [ExternalDNS for Services on AWS](https://github.com/kubernetes-incubator/external-dns/blob/master/docs/tutorials/aws.md)

### Overview

Traefik is an Edge-Router or Reverse-Proxy, that works with queries from the
internet and redirects them to services in your cluster. The main components
in this setup (the concepts changed from v1 to v2) are:

* **EntryPoints**:  The ports and hostnames from which your site can be accessed
* **Routers**: The process that decides which entrypoint goes to which service
 in your cluster
* **Middleware**: A process that transforms or does checks on the signal that
is coming from the router to the service. Like authenticating or redirecting
* **Services**: The way in which Traefik talks to the actual servers
where the apps are located. We won't be using it much, because
we are on a single K8-cluster.

Overall it looks something like this:

<img src="docs/assets/traefik.png"/>

\
Now we will see the resources that have to be applied in the order in which
they have to be applied. **The order is important because
of the Let's Encrypt Challenge**:

**If you already have a traefik deployment you skip right to the ingress part
because you only have to give a subdomain to the service you want to expose**

### CRD and Roles

Traefik designed Custom Resource Definitions (CRD) for K8 to define the routes
in their own updatable manifest files. The actual monitoring and handling of
everything (ingress controller) is done by a deployment that has to be granted
certain permissions, hence the use of ClusterRoles. The CRD's and Roles can
be applied to k8 by running (This file needs no customization for our cluster.):

`kubectl apply -f kubernetes/traefik/custom_resourcedef_and_cr.yaml`

### Service

The service uses the LoadBalancer feature of k8 in AWS
that automatically creates an Elastic Load Balancer (ELB).
It has to have the ports that your application will be
accessed from over the internet open.
We also added an annotation for ExternalDNS, that will make sense later.

`kubectl apply -f kubernetes/traefik/services.yaml`

### ExternalDNS

Based on [here](https://github.com/kubernetes-sigs/external-dns/blob/master/docs/tutorials/aws.md)
Before actually activating the traefik routers (which gets activated
once the controller detects an ingress) we must get or
create a hosted zone and assign it a public hostname from Route 53 or
from another DNS registrar, but with Route 53 as its DNS zone.

First we save the domain name in a variable:
`export DNS_NAME=zygoo.mx`

There are two things you can do. Create a hosted zone registered in Route 53.
That can be done with this
[command](https://docs.aws.amazon.com/cli/latest/reference/route53domains/register-domain.html):

```bash
aws route53domains register-domain \
--domain-name $DNS_NAME \
--duration-in-years <value> \
--admin-contact <value> \
--registrant-contact <value> \
--tech-contact <value>
```

 or in the Route53 service in the AWS console. If you have a domain
 registered elsewhere you must use Route 53 as your DNS Service.
 To do that you have to create a hosted zone with the name of domain
 you registered.
 `aws route53 create-hosted-zone --name "$DNS_NAME" --caller-reference "$DNS_NAME-$(date +%s)"`

The caller reference ensures that you can run the command multiple
times and it is not created twice.

Make a note of the ID of the hosted zone you just created,
which will serve as the value for my-hostedzone-identifier.
`export ZONE_ID=$(aws route53 list-hosted-zones-by-name --output json --dns-name $DNS_NAME | jq -r '.HostedZones[0].Id')`

Make a note of the nameservers that were assigned to your new zone.

```bash
aws route53 list-resource-record-sets --output json --hosted-zone-id $ZONE_ID \
--query "ResourceRecordSets[?Type == 'NS']" | jq -r '.[0].ResourceRecords[].Value'
```

You will have to input this nameservers in your domain registrar, like godaddy.
This configuration can take a whole day to function.

IT IS IMPORTANT TO REMOVE THE DOTS AT THE END OF THE NAMESERVER, OR ELSE IT WONT WORK.

From now on it doesn't matter where you registered your domain.
You just have to have the `$ZONE_ID` and `$DNS_NAME` vars declared.

ExternalDNS needs some special permissions that aren't normally
assigned to the role of the EKS cluster. These permissions can be
added with this json:

```bash
{
 "Version": "2012-10-17",
 "Statement": [
   {
     "Effect": "Allow",
     "Action": [
       "route53:ChangeResourceRecordSets"
     ],
     "Resource": [
       "arn:aws:route53:::hostedzone/*"
     ]
   },
   {
     "Effect": "Allow",
     "Action": [
       "route53:ListHostedZones",
       "route53:ListResourceRecordSets"
     ],
     "Resource": [
       "*"
     ]
   }
 ]
}
```

Save it to a file e.g. `perms.json`. This needs to be added to your
nodegroup role, so to get the ARN (Amazon Resource Name) of that role you can run:

`export NODE_ROLENAME=$(aws iam list-roles --output json | jq -r '.Roles[] | select(.RoleName|test("node")) | .RoleName')`

And then add the role via this command:
`aws iam put-role-policy --role-name $NODE_ROLENAME --policy-name ExternalDNS --policy-document file://perms.json`

Then in the file `kubernetes/traefik/external_dns.yaml` change the value
of `--txt-owner-id` to your `$ZONE_ID` and apply it:

`kubectl apply -f kubernetes/traefik/external_dns.yaml`

If you have more than two domains make two of these deployments.

After roughly two minutes check that a corresponding DNS record for,
your service was created.

```bash
aws route53 list-resource-record-sets --output json --hosted-zone-id $ZONE_ID \
    --query "ResourceRecordSets[?Name == '$DNS_NAME.']|[?Type == 'A']"
```

The ExternalDNs pod checks the annotations of the service for the
names you declared. I declared a wildcard so that we can choose any
subdomain of the type "\*.zygoo.mx". The subdomain alias is created automatically.

If you want to add another domain name, you only have to upload another
deployment with another name and the new ZONE_ID.

### Ingress

Now that your names are public and can be accessed by Let's Encrypt,
we can deploy the Routers that assigns paths and/or subdomains to
your Services.

`kubectl apply -f kubernetes/traefik/ingress_route.yaml`

This defines the middleware that is going to redirect http traffic to https
first and then it defines the routers.

The site should then be accessible through the hostnames you provided
and be redirecting http traffic to https.

### Deployment

Our deployment will use a dynamic configuration file that we will provide
via a ConfigMap. The file is normally named `traefik.yaml`. And we deploy
the map directly with this command:

`kubectl create configmap traefik-conf --from-file=kubernetes/traefik/traefik.yaml`

Now we can deploy Traefik itself. And this it the reason why we deployed some
communication/security rules before. Traefik is basically just a common
Deployment which communicates with the Kubernetes API and adjusts its
configuration on the fly to match your requirements defined in the
custom Kubernetes objects.

We could use K8's DaemonSet's, which are pods that are deployed
in every node for the ingress controller.
However, when the platform (like AWS) the cluster is in, can
automatically create loadbalancers, the service for the Ingress
Controller deployment can easily communicate with every other node
and deploys are easier to scale.

`kubectl apply -f kubernetes/traefik/deployment.yaml`

The deployment uses annotations to instruct the image to use
the Let's Encrypt algorithm for TLS certification (using https).
That is why you'll have to input your own mail in this part:

```yaml
args:
  - --api.insecure
  - --accesslog
  - --entrypoints.web.Address=:80
  - --entrypoints.websecure.Address=:443
  - --providers.kubernetescrd
  - --certificatesresolvers.default.acme.tlschallenge
  - --certificatesresolvers.default.acme.email=paquidios@gmail.com
  - --certificatesresolvers.default.acme.storage=acme.json
```

Also the names for the ports `web` and `websecure` are yours to
decide, but be sure to use them consistently in the other files.
`api.insecure` tells the app that the dashboard for traefik can
be accessed without credentials and other features, **this
shouldn't  be allowed in production**. `accesslog` enables logs
for the routers and services, tracing and metrics are other
features.

<a name="Clean"></a>

## Cleaning up

To delete the cluster:
`eksctl delete cluster --name=cactus-eksctl \
`

To delete the database:
`aws rds delete-db-instance \
--skip-final-snapshot \
--db-instance-identifier ${RDS_DATABASE_NAME} \
--region ${AWS_REGION} \
 \
&& aws rds delete-db-subnet-group --db-subnet-group-name default --profile=$PROF`

To delete the vpc:
`aws ec2 delete-vpc-peering-connection --vpc-peering-connection-id $PEER_VPC --profile=$PROF`

Lastly delete the security group:
`delete-security-group --group-id $PEER_VPC`

<a name="Troubleshooting"></a>

## Troubleshooting

Remember that kubernetes has a copy of the images used in the master node.
If you don't want to be changing tags all the time, you can create a job
with the key `imagePullPolicy: Always`. Just after the image key, like this:

```bash
containers:
  - name: django
    image: paquidios/inguz:cactus0.1
    imagePullPolicy: Always
```

Images are automatically deleted by the garbage collector in the kubelets.
Based on some criteria like, max. space used, etc. See:
<https://kubernetes.io/docs/concepts/cluster-administration/kubelet-garbage-collection/>
for more info.

If you exit your context because of using minikube. You can search for it using:
`kubectl config get-contexts`

And then assign it:
`kubectl config set current-context Administrator@cactus-eksctl.us-east-2.eksctl.io`

The contexts are written in a file in `~/.kube/config`

It is best to create a service prior to any controllers (like a deployment) so
that the Kubernetes scheduler can distribute the pods for the service as they
are created by the controller.

For the difference between LoadBalancer, NodePort and ClusterIP se
[here](https://medium.com/google-cloud/kubernetes-nodeport-vs-loadbalancer-vs-ingress-when-should-i-use-what-922f010849e0)

In AWS accounts that have never created a load balancer before, it’s possible
 that the service role for ELB might not exist yet.

We can check for the role, and create it if it’s missing.

Copy/Paste the following commands into your AWS CLI:

`aws iam get-role --role-name "AWSServiceRoleForElasticLoadBalancing" || aws iam create-service-linked-role --aws-service-name "elasticloadbalancing.amazonaws.com"`

It is expected for this to show an error, because it checks if the role exists.

Esta cheatsheet ayuda mucho: <https://kubernetes.io/docs/reference/kubectl/cheatsheet/#kubectl-context-and-configuration>
Si el deployment no encuentra las imágenes no te jalan con esto,
puede ser que no estés dentro del docker daemon. Las imágenes que creaste
dentro del docker daemon de minikube se
quedan ahí, así que te debes de meter así `eval $(minikube docker-env)`
para poder acceder. Además, puedes correr esto:

`kubectl config use-context minikube`

Para ver si hay un error en los containers y porque, primero obtén el nombre del pod:

`kubectl get pod`

y luego saca su log con:

 `kubectl --v=8 logs <nombre-pod>`

Además, puedes correr comandos dentro de la imagen para ver que puede estar mal,
pero ten cuidado que en realidad estas haciendo un container temporal, no
harás cambios a la imagen en general.

`docker run --rm -it paquidios/inguz:cactus0.1 /bin/bash`

If you cant enter with `/bin/bash` just use `sh`

Y si no quieres que se corra el server, overrideas el entrypoint de esta manera:

`docker run --rm -it --entrypoint "/bin/bash" paquidios/inguz:cactus0.1`

Y si quieres acceder al pod ya en el cluster:

`kubectl exec -it cactus-site-c8dd466bd-7lf88 -- /bin/bash`

Te puede servir este comando que accede al primer pod en la lista de pods,
 cuyo label sea app:web:

`kubectl exec -it $(kubectl get pod -l app=web -o jsonpath="{.items[0].metadata.name}") -- /bin/bash`

Borrar las imagenes sin nombre:
`docker rmi $(docker images -f dangling=true -q)`

Meterte a la base de datos postgresql del deployment de postgres
`kubectl exec -it $(kubectl get pod -l app=postgres-container -o jsonpath="{.items[0].metadata.name}") -- /bin/bash`

`psql -U admin -d postgres`

If you dont have enoguh wokrer nodes follow this guide to migrate to a nodegroup
with bigger instances:
<https://docs.aws.amazon.com/eks/latest/userguide/migrate-stack.html>

 Or you can also adjust the desired instances in the auto
scaling site in the aws console.
