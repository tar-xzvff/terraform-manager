from rest_framework import routers

from api.views.terraform_file import TerraformFileViewSet, CeleryExampleViewSet

router = routers.SimpleRouter()
router.register(r'terraform_files', TerraformFileViewSet)
router.register(r'celery_example', CeleryExampleViewSet, base_name="celery-example")
#router.register(r'accounts', AccountViewSet)
urlpatterns = router.urls
