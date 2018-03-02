from common.models.terraform_file import TerraformFile
from common.models.environment import Environment
from rest_framework import serializers


class TerraformFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TerraformFile
        fields = ('id', 'name', 'body', 'created_at', 'updated_at',)


class EnvironmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Environment
        fields = ('id', 'terraform_file',)
        read_only_fields = ('id', 'created_at', 'updated_at',)

    def create(self, validated_data):
        environment = Environment.objects.create(**validated_data)
        from common.common_tasks import copy_tf_files
        copy_tf_files.delay(environment.id, environment.terraform_file.id)
        return environment
