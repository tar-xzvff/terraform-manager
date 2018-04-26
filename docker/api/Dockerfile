FROM ubuntu:16.04

# Python3実行環境のインストール.
RUN apt-get update \
  && apt-get install -y python3-pip python3-dev curl nginx \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

# ライブラリのインストール.
RUN mkdir /terraform-manager
WORKDIR /terraform-manager/
COPY ./requirements.txt /terraform-manager/
RUN pip3 install -r requirements.txt

# ソースファイルのコピー.
COPY ./ /terraform-manager/

ENV PYTHONPATH /terraform-manager/terraform_manager:$PYTHONPATH
CMD ["uwsgi","--http",":80","--file","/terraform-manager/terraform_manager/terraform_manager/wsgi.py"]
