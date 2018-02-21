from rest_framework import routers

from api.views.terraform_file import TerraformFileViewSet

router = routers.SimpleRouter()
router.register(r'terraform_files', TerraformFileViewSet)
#router.register(r'accounts', AccountViewSet)
urlpatterns = router.urls
