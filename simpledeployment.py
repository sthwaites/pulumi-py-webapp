from pulumi_kubernetes.apps.v1 import Deployment
from pulumi_kubernetes.core.v1 import Service
from pulumi import ComponentResource, ResourceOptions, Output

# References
# https://github.com/pulumi/examples/blob/master/kubernetes-py-guestbook/components/service_deployment.py

class SimpleDeployment(ComponentResource):

    def __init__(self,
                 name : str,
                 replicas: int = 1,
                 image : str = None,
                 ports: [int] = None,
                 envvars: [dict] = None,
                 opts: ResourceOptions = None):
        
        super().__init__("my:modules:SimpleDeployment", name, {}, opts)

        labels = {"app": name}
        container = {
            "name": name,
            "image": image,
            "ports": [{"container_port": p} for p in ports] if ports else None,
            "env" : envvars,
        }

        self.deployment = Deployment(
            name,
            spec={
                "selector": {"match_labels": labels},
                "replicas": replicas,
                "template": {
                    "metadata": {"labels" : labels},
                    "spec" : {"containers": [container]},
                },
            },
            opts=ResourceOptions(parent=self)
        )
        
        self.service = Service(
            name,
            metadata={
                "name": name,
                "labels": self.deployment.metadata['labels'],
            },
            spec={
                "ports": [{"port": p, "targetPort": p} for p in ports] if ports else None,
                "selector": self.deployment.spec['template']['metadata']['labels'],
                "type": "LoadBalancer",
            },
            opts=ResourceOptions(parent=self)
        )

        self.register_outputs({})