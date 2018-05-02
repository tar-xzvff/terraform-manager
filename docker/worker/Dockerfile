FROM fedora:26

# terraformのインストール
WORKDIR /bin/
RUN yum install -y curl unzip python3-devel
RUN yum groupinstall -y "Development Tools"
RUN curl -sL https://releases.hashicorp.com/terraform/0.11.7/terraform_0.11.7_linux_amd64.zip > terraform.zip
RUN unzip terraform.zip
RUN curl -sL https://github.com/sacloud/terraform-provider-sakuracloud/releases/download/v1.0.5/terraform-provider-sakuracloud_1.0.5_linux-amd64.zip > terraform_sackuracloud.zip
RUN unzip terraform_sackuracloud.zip

# ライブラリのインストール.
RUN mkdir /terraform-manager
WORKDIR /terraform-manager/
COPY ./requirements.txt /terraform-manager/
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt


# ソースファイルのコピー.
COPY ./ /terraform-manager/

# terraform実行環境のディレクトリを作成.
RUN mkdir /terraform-environment

WORKDIR /terraform-manager/terraform_manager/
ENV PYTHONPATH /terraform-manager/terraform_manager:$PYTHONPATH
CMD celery -A common.common_tasks worker --loglevel=info

#   TODO    :   redisとDB接続先とterraform実行環境のパスを外部から変数として設定できるようにする.
