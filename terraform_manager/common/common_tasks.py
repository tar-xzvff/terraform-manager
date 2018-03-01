from __future__ import absolute_import, unicode_literals
import os, logging
from celery import Celery
from python_terraform import Terraform

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'terraform_manager.settings')

app = Celery('terraform_manager')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks()

TERRAFORM_PATH = ''
TERRAFORM_ENVIRONMENT_ROOT_PATH = ''


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


def get_app():
    return app


@app.task
def copy_tf_files(environment_id, terraform_file_id):
    environment_dir = TERRAFORM_ENVIRONMENT_ROOT_PATH + str(environment_id)

    import os
    os.mkdir(environment_dir)

    from common.models.terraform_file import TerraformFile
    tf = TerraformFile.objects.get(id=terraform_file_id)
    f = open(environment_dir + "/" + '{}.tf'.format(tf.name), 'w')
    f.writelines(tf.body)
    f.close()


@app.task
def init(environment_id):
    tf = Terraform(working_dir=TERRAFORM_ENVIRONMENT_ROOT_PATH + str(environment_id))
    return_code, stdout, stderr = tf.init()
    # 不具合があるので一旦コメントアウト
    #from common.models.log import Log
    from common.models.environment import Environment
    #log = Log(environment=Environment.objects.get(id=environment_id),
    #          return_code=return_code,
    #          stdout=stdout,
    #          stderr=stderr)
    #log.save()


@app.task
def plan(self, id, var):
    tf = Terraform(working_dir=TERRAFORM_ENVIRONMENT_ROOT_PATH + id)
    return_code, stdout, stderr = tf.plan(var=var)
    from common.models.log import Log
    log = Log(environment=id,
              return_code=return_code,
              stdout=stdout,
              stderr=stderr)
    log.save()


@app.task
def apply(self, id, var):
    tf = Terraform(working_dir=TERRAFORM_ENVIRONMENT_ROOT_PATH + id)
    return_code, stdout, stderr = tf.apply(var=var)
    from common.models.log import Log
    log = Log(environment=id,
              return_code=return_code,
              stdout=stdout,
              stderr=stderr)
    log.save()


@app.task
def destroy(self, id, var):
    tf = Terraform(working_dir=TERRAFORM_ENVIRONMENT_ROOT_PATH + id)
    return_code, stdout, stderr = tf.destroy(var=var)
    from common.models.log import Log
    log = Log(environment=id,
              return_code=return_code,
              stdout=stdout,
              stderr=stderr)
    log.save()
