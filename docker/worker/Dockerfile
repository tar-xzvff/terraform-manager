FROM ubuntu:16.04

# Python3実行環境のインストール.
RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

# terraformのインストール
WORKDIR /bin/
RUN apt-get install -y curl unzip
RUN curl -sL https://releases.hashicorp.com/terraform/0.11.7/terraform_0.11.7_linux_amd64.zip > terraform.zip
RUN unzip terraform.zip
RUN curl -sL https://releases.usacloud.jp/terraform/terraform-provider-sakuracloud_1.0.5_linux-amd64.zip > terraform_sackuracloud.zip
RUN unzip terraform_sackuracloud.zip

# ライブラリのインストール.
RUN mkdir /terraform-manager
WORKDIR /terraform-manager/
COPY ./requirements.txt /terraform-manager/
RUN pip3 install -r requirements.txt


# ソースファイルのコピー.
COPY ./ /terraform-manager/

# terraform実行環境のディレクトリを作成.
RUN mkdir /terraform-environment

WORKDIR /terraform-manager/terraform_manager/
ENV PYTHONPATH /terraform-manager/terraform_manager:$PYTHONPATH
CMD celery -A common.common_tasks worker --loglevel=info