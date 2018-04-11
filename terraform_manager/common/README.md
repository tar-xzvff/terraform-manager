## celery worker
非同期処理をceleryで処理します.

### 1.Install Python3 (CentOS)

```bash
curl -O https://www.python.org/ftp/python/3.5.1/Python-3.5.1.tgz
tar zxf Python-3.5.1.tgz
cd Python-3.5.1
./configure --prefix=/usr/local
make
make altinstall
```

### 1.Install Python3 (Ubuntu)
```bash
sudo apt-get update -y
sudo apt install -y python3-pip
sudo pip3 install virtualenv
virtualenv ~/virtualenv
source ~/virtualenv/bin/activate
```

### 2.Install Redis (Mac)
```
brew install redis
redis-server /usr/local/etc/redis.conf
```

### Run

```bash
git clone https://github.com/tar-xzvff/terraform-manager.git
cd terraform-manager
pip install -r requirements.txt
cd terraform_manager/common
#DjangoプロジェクトのフルパスをPYTHONPATHに設定 (以下はubuntuの場合を想定)
export PYTHONPATH=/home/ubuntu/terraform-manager/terraform_manager/
celery -A common.common_tasks worker --loglevel=info
```