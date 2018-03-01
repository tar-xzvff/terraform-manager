from rest_framework import viewsets

from common.models.terraform_file import TerraformFile
from common.models.environment import Environment

from api.serializers.terraform_file import TerraformFileSerializer
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from api.serializers.environment import EnvironmentSerializer


class TerraformFileViewSet(viewsets.ModelViewSet):
    queryset = TerraformFile.objects.all()
    serializer_class = TerraformFileSerializer

    @detail_route(methods=['post'])
    def create_environment(self, *args, **kwargs):
        from api.serializers.environment import EnvironmentSerializer
        data = {"terraform_file": kwargs['pk'], 'state': 'none'}
        serializer = EnvironmentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.error_messages)


class EnvironmentViewSet(viewsets.ModelViewSet):
    queryset = Environment.objects.all()
    serializer_class = EnvironmentSerializer

    @detail_route(methods=['put'])
    def init(self, *args, **kwargs):
        from common.common_tasks import init
        init.delay(self.get_object().id)
        return Response()

    @detail_route(methods=['put'])
    def plan(self, *args, **kwargs):
        pass

    @detail_route(methods=['put'])
    def apply(self, *args, **kwargs):
        pass

    @detail_route(methods=['put'], url_path='destroy')
    def _destroy(self, *args, **kwargs):
        pass


class CeleryExampleViewSet(viewsets.ViewSet):
    def list(self, request):
        from common.common_tasks import debug_task
        debug_task.delay()
        return Response()
