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
def init(self, id):
    tf = Terraform(working_dir=TERRAFORM_ENVIRONMENT_ROOT_PATH + id)
    tf.init()


@app.task
def plan(self, id):
    tf = Terraform(working_dir=TERRAFORM_ENVIRONMENT_ROOT_PATH + id)
    tf.plan()


@app.task
def apply(self, id):
    tf = Terraform(working_dir=TERRAFORM_ENVIRONMENT_ROOT_PATH + id)
    tf.apply()


@app.task
def destroy(self, id):
    tf = Terraform(working_dir=TERRAFORM_ENVIRONMENT_ROOT_PATH + id)
    tf.destroy()
