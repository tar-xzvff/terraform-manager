# terraform-manager

## How to run

### API
```
git clone https://github.com/tar-xzvff/terraform-manager.git
pip install -r requirements.txt
cd terraform_manager/
python manage.py migrate
python manage.py runserver
```

### worker
https://github.com/tar-xzvff/terraform-manager/tree/master/terraform_manager/common


## Deployment
### workerコンテナの作成方法
```
# プロジェクトのルートディレトリで以下のコマンドを実行
docker build -t terraform-manager-worker  -f docker/worker/Dockerfile .
```