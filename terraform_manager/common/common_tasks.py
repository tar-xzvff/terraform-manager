from __future__ import absolute_import, unicode_literals
import os
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
def copy_tf_files(self, id):
    #   TODO    :   TFファイルをテキストのからファイルにして、任意のディレクトリに保存する処理を実装する
    pass


@app.task
def init(self, id):
    tf = Terraform(working_dir=TERRAFORM_ENVIRONMENT_ROOT_PATH + id)
    return_code, stdout, stderr = tf.init()
    from common.models.log import Log
    log = Log(id=id,
              return_code=return_code,
              stdout=stdout,
              stderr=stderr)
    log.save()


@app.task
def plan(self, id, var):
    tf = Terraform(working_dir=TERRAFORM_ENVIRONMENT_ROOT_PATH + id)
    return_code, stdout, stderr = tf.plan(var=var)
    from common.models.log import Log
    log = Log(id=id,
              return_code=return_code,
              stdout=stdout,
              stderr=stderr)
    log.save()


@app.task
def apply(self, id, var):
    tf = Terraform(working_dir=TERRAFORM_ENVIRONMENT_ROOT_PATH + id)
    return_code, stdout, stderr = tf.apply(var=var)
    from common.models.log import Log
    log = Log(id=id,
              return_code=return_code,
              stdout=stdout,
              stderr=stderr)
    log.save()


@app.task
def destroy(self, id, var):
    tf = Terraform(working_dir=TERRAFORM_ENVIRONMENT_ROOT_PATH + id)
    return_code, stdout, stderr = tf.destroy(var=var)
    from common.models.log import Log
    log = Log(id=id,
              return_code=return_code,
              stdout=stdout,
              stderr=stderr)
    log.save()
