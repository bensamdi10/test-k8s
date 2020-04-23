from rest_framework.serializers import ModelSerializer

from container.models import Container
from deployment.models import Deployment, ClusterIP
from environnement.models import Environnement
from ingress.models import Ingress
from job.models import Job
from project.models import Project
from service.models import Service
from store.models import Variable, Path, Template, PersistentVolume


class ContainerSerializer(ModelSerializer):
    class Meta:
        model = Container
        fields = ['id', 'uid', 'name', "type", "base_image", "image_name", "source", "port", "volume_path", "commands", "cmd", "color", "color_fade", "deployment", "variable", "persistent_volume" ]

class DeploymentSerializer(ModelSerializer):
    class Meta:
        model = Deployment
        fields = ['id', "uid", 'name', "replicas", "persistent_volume", "environnement", "color", "color_fade" ]

class ClusterIPSerializer(ModelSerializer):
    class Meta:
        model = ClusterIP
        fields = ['id', "uid", 'name', "deployment", "port", "environnement", "color", "color_fade" , "slug"]

class EnvironnementSerializer(ModelSerializer):
    class Meta:
        model = Environnement
        fields = ['id', "uid", 'name', "type", "variable", "persistent_volume", "current", "color", "color_fade" ]

class IngressSerializer(ModelSerializer):
    class Meta:
        model = Ingress
        fields = ['id', 'domain', "accept_tls", "accept_ssl", "uid", "ip_address", "path", "annotations", "environnement", "container" ]

class JobSerializer(ModelSerializer):
    class Meta:
        model = Job
        fields = ['id',"name", "schedule", "restart_policy", "uid", "environnement", "command", "container", "type", "back_off_limit", "config", "container_image" ]

class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', "name_space", "provider", "uid", "current" ]

class ServiceSerializer(ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', "uid", "environnement", "variable", "before_install", "script", "after_success", "deploy", "type", "on_branch"  ]

class VariableSerializer(ModelSerializer):
    class Meta:
        model = Variable
        fields = ['id', 'name', "value", "uid", "secret", "slug" ]

class PathSerializer(ModelSerializer):
    class Meta:
        model = Path
        fields = ['id', 'name', "path", "port", "uid" ]

class TemplateSerializer(ModelSerializer):
    class Meta:
        model = Template
        fields = ['id', 'name', "description", "type", "uid", "data" ]

class PersistentVolumeSerializer(ModelSerializer):
    class Meta:
        model = PersistentVolume
        fields = ['id', 'name', "description", "access_mode", "storage", "uid", "volume_mode", "storage_class", "mount_path", "sub_path", "selector"  ]