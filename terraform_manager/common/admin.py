from django.contrib import admin

from common.models import Log, Variable
from common.models.environment import Environment
from common.models.terraform_file import TerraformFile


admin.site.register(Log)
admin.site.register(Variable)
admin.site.register(Environment)
admin.site.register(TerraformFile)
