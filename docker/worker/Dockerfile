FROM ubuntu:16.04

# Python3実行環境のインストール.
RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

# ソースファイルのコピー.
RUN mkdir /terraform-manager
COPY ./ /terraform-manager/

# ライブラリのインストール.
WORKDIR /terraform-manager/
RUN pip3 install -r requirements.txt

WORKDIR /terraform-manager/terraform_manager/
ENV PYTHONPATH /terraform-manager/terraform_manager:$PYTHONPATH
CMD celery -A common.common_tasks worker --loglevel=info