from rest_framework import viewsets

from common.models.terraform_file import TerraformFile

from api.serializers.terraform_file import TerraformFileSerializer


class TerraformFileViewSet(viewsets.ModelViewSet):
    queryset = TerraformFile.objects.all()
    serializer_class = TerraformFileSerializer
