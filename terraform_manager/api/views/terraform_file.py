from rest_framework import viewsets

from common.models.terraform_file import TerraformFile
from common.models.environment import Environment

from api.serializers.terraform_file import TerraformFileSerializer
from rest_framework.decorators import detail_route
from rest_framework.response import Response


class TerraformFileViewSet(viewsets.ModelViewSet):
    queryset = TerraformFile.objects.all()
    serializer_class = TerraformFileSerializer

    @detail_route(methods=['post'])
    def create_environment(self, *args, **kwargs):
        from api.serializers.environment import EnvironmentSerializer
        data = {"terraform_file": kwargs['pk']}
        serializer = EnvironmentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            print("VALID")
            return Response()
        else:
            print("INVALID")
            return Response()


class EnvironmentViewSet(viewsets.ModelViewSet):
    queryset = Environment.objects.all()
    serializer_class = TerraformFileSerializer
