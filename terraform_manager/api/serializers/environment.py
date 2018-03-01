from rest_framework import serializers

from common.models.environment import Environment


class EnvironmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Environment
        fields = ('id', 'terraform_file', )
        read_only_fields = ('id', 'created_at', 'updated_at', )

    def create(self, validated_data):
        environment = Environment.objects.create(**validated_data)
        from common.common_tasks import copy_tf_files
        copy_tf_files.delay(environment.id, environment.terraform_file.id)
        return environment
