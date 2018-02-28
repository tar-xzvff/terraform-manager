from rest_framework import viewsets

from common.models.terraform_file import TerraformFile
from common.models.environment import Environment

from api.serializers.terraform_file import TerraformFileSerializer
from rest_framework.response import Response


class TerraformFileViewSet(viewsets.ModelViewSet):
    queryset = TerraformFile.objects.all()
    serializer_class = TerraformFileSerializer


class EnvironmentViewSet(viewsets.ModelViewSet):
    queryset = Environment.objects.all()
    serializer_class = TerraformFileSerializer


class CeleryExampleViewSet(viewsets.ViewSet):
    def list(self, request):
        from common.common_tasks import debug_task
        debug_task.delay()
        return Response()
