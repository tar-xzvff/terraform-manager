from __future__ import absolute_import, unicode_literals
import os, logging
from celery import Celery
from python_terraform import Terraform


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'terraform_manager.settings.develop')

app = Celery('terraform_manager')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks()

TERRAFORM_PATH = ''
TERRAFORM_ENVIRONMENT_ROOT_PATH = '/terraform-environment/'


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


def get_app():
    return app


@app.task
def copy_tf_files(environment_id, terraform_file_id):
    """
    terraformの実行に必要なファイルをworkerのカレントディレクトリにコピーします.
    :param environment_id:  環境ID
    :param terraform_file_id:   terraformファイルID
    """
    prepare_environment(environment_id, terraform_file_id)


@app.task
def init(environment_id):
    """
    terraform initを実行します.
    :param environment_id:  環境ID
    """
    from common.models.environment import Environment
    environment = Environment.objects.get(id=environment_id)

    if not os.path.isdir(TERRAFORM_ENVIRONMENT_ROOT_PATH + environment_id):
        prepare_environment(environment_id=environment_id, terraform_file_id=environment.terraform_file.id)
    environment.locked = True
    environment.save()
    try:
        tf = Terraform(working_dir=TERRAFORM_ENVIRONMENT_ROOT_PATH + str(environment_id))
        return_code, stdout, stderr = tf.init()
        save_log(environment_id, return_code, stdout, stderr)
    except:
        #   TODO    :   エラーログを送出する
        pass
    finally:
        environment.locked = False
        environment.save()


@app.task
def plan(environment_id, var):
    """
    terraform planを実行します.
    :param environment_id:  環境ID
    :param var: terraformコマンド実行時に引数に渡す変数
    """
    from common.models.environment import Environment
    environment = Environment.objects.get(id=environment_id)

    import os
    if not os.path.isdir(TERRAFORM_ENVIRONMENT_ROOT_PATH + environment_id):
        prepare_environment(environment_id, environment.terraform_file.id)
        init(environment_id)
    if environment.locked:
        # ロックしているときはコマンドを実行しない.
        raise Exception()

    environment.locked = True
    environment.save()
    try:
        tf = Terraform(working_dir=TERRAFORM_ENVIRONMENT_ROOT_PATH + str(environment_id))
        return_code, stdout, stderr = tf.plan(var=var)
        save_log(environment_id, return_code, stdout, stderr)
    except:
        #   TODO    :   エラーログを送出する
        pass
    finally:
        environment.locked = False
        environment.save()


@app.task
def apply(environment_id, var):
    """
    terraform applyを実行します.
    :param environment_id:  環境ID
    :param var: terraformコマンド実行時に引数に渡す変数
    """
    from common.models.environment import Environment
    environment = Environment.objects.get(id=environment_id)

    import os
    if not os.path.isdir(TERRAFORM_ENVIRONMENT_ROOT_PATH + environment_id):
        prepare_environment(environment_id, environment.terraform_file.id)
        init(environment_id)
    if environment.locked:
        # ロックしているときはコマンドを実行しない.
        raise Exception()

    environment.locked = True
    environment.save()
    try:
        import os
        os.environ["TF_CLI_ARGS"] = "-auto-approve=true"
        tf = Terraform(working_dir=TERRAFORM_ENVIRONMENT_ROOT_PATH + str(environment_id))
        return_code, stdout, stderr = tf.apply(var=var)
        os.environ.pop("TF_CLI_ARGS")
        save_log(environment_id, return_code, stdout, stderr)
    except:
        #   TODO    :   エラーログを送出する
        pass
    finally:
        environment.locked = False
        environment.save()


@app.task
def destroy(environment_id, var):
    """
    terraform destroyを実行します.
    :param environment_id:  環境ID
    :param var: terraformコマンド実行時に引数に渡す変数
    """
    #   TODO    :   マルチノードの場合、正常に処理が実行されないので、backendを指定してステータスを管理する.
    from common.models.environment import Environment
    environment = Environment.objects.get(id=environment_id)

    import os
    if not os.path.isdir(TERRAFORM_ENVIRONMENT_ROOT_PATH + environment_id):
        prepare_environment(environment_id, environment.terraform_file.id)
        init(environment_id)
    if environment.locked:
        # ロックしているときはコマンドを実行しない.
        raise Exception()

    environment.locked = True
    environment.save()
    try:
        import os
        os.environ["TF_CLI_ARGS"] = "-auto-approve=true"
        tf = Terraform(working_dir=TERRAFORM_ENVIRONMENT_ROOT_PATH + str(environment_id))
        return_code, stdout, stderr = tf.destroy(var=var)
        os.environ.pop("TF_CLI_ARGS")
        save_log(environment_id, return_code, stdout, stderr)
    except:
        #   TODO    :   エラーログを送出する
        pass
    finally:
        environment.locked = False
        environment.save()


def prepare_environment(environment_id, terraform_file_id):
    """
    terraform実行環境を作成します.
    :param environment_id:  環境ID
    :param terraform_file_id:   TerraformファイルID
    """

    # ディレクトリの作成.
    environment_dir = TERRAFORM_ENVIRONMENT_ROOT_PATH + str(environment_id)
    os.mkdir(environment_dir)

    # *.tfファイルのコピー.
    from common.models.terraform_file import TerraformFile
    tf = TerraformFile.objects.get(id=terraform_file_id)
    f = open(environment_dir + "/" + '{}.tf'.format(tf.file_name), 'wb')
    f.write(tf.body.encode('utf-8'))
    f.close()

    # ShellScriptのコピー
    if tf.has_shell_script():
        for script in tf.shell_script.all():
            f = open(environment_dir + "/" + '{}.sh'.format(script.file_name), 'wb')
            f.write(script.body.encode('utf-8'))
            f.close()

    # 変数定義ファイルの作成.
    variables_tf = """
provider "sakuracloud" {
    # APIキー(トークン)
    token = "${var.token}"
    # APIキー(シークレット)
    secret = "${var.secret}"
    # デフォルトゾーン
    zone = "${var.zone}"
}
variable "token" {}
variable "secret" {}
variable "zone" {}
    """
    f = open(environment_dir + "/" + '{}.tf'.format("variables"), 'wb')
    f.write(variables_tf.encode('utf-8'))
    f.close()


def save_log(environment_id, return_code, stdout, stderr):
    """
    ログを保存します.
    :param environment_id:
    :param return_code:
    :param stdout:
    :param stderr:
    """
    from common.models import Log
    from common.models.environment import Environment
    log = Log(environment=Environment.objects.get(id=environment_id),
              return_code=return_code,
              stdout=stdout,
              stderr=stderr)
    log.save()
