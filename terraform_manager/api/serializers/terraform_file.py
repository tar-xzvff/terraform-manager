from rest_framework import serializers

from common.models.terraform_file import TerraformFile


class TerraformFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TerraformFile
        fields = ('id', 'name', 'body', 'created_at', 'updated_at', )
