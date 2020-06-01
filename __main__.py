import base64
import pulumi
import pulumi_aws as aws
import pulumi_docker as docker
from pulumi import ResourceOptions
from simpledeployment import SimpleDeployment

config = pulumi.Config()
message = config.require('webapp_message')
image_name = config.require('image_name')

# Ref: https://github.com/pulumi/pulumi-docker/blob/master/examples/aws-py/__main__.py

# Get registry info (creds and endpoint) so we can build/publish to it.
def get_registry_info(rid):
    creds = aws.ecr.get_credentials(registry_id=rid)
    decoded = base64.b64decode(creds.authorization_token).decode()
    parts = decoded.split(':')
    if len(parts) != 2:
        raise Exception("Invalid credentials")
    return docker.ImageRegistry(creds.proxy_endpoint, parts[0], parts[1])

# Create a private ECR registry.
repo = aws.ecr.Repository(image_name, name=image_name)

registry = repo.registry_id.apply(get_registry_info)

image_tag = repo.repository_url.apply(lambda url: url + ":latest")

# Build and publish the image.
build_image = docker.Image(
    image_name,
    build=docker.DockerBuild(context='app'),
    image_name=image_tag,
    registry=registry,
#    opts=ResourceOptions(aliases="hw_image")
)

# Deployment based on simpledeployment 
helloworldapp = SimpleDeployment(
    "helloworld",
    replicas=2, 
    image=image_tag, 
    ports=[80],
    envvars=[{"name" : "MESSAGE", "value" : message}],
    opts=ResourceOptions(depends_on=[build_image])
)

# Exports
pulumi.export("image_name", image_name)
pulumi.export("image_tag", image_tag)
pulumi.export("repo_url", repo.repository_url)