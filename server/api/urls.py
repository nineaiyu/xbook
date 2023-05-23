from django.urls import include, re_path
from rest_framework.routers import SimpleRouter

from api.views.aliyundrive import AliyunDriveQRView, AliyunDriveView
from api.views.auth import LoginView, LogoutView, UserInfoView, RefreshTokenView, FingerprintLoginView
from api.views.download import DownloadView
from api.views.files import FileInfoView, ManyView
from api.views.upload import AliyunDriveUploadView

router = SimpleRouter(False)
router.register('drive', AliyunDriveView)
router.register('file', FileInfoView)
router.register('download', DownloadView)
urlpatterns = [
    re_path(r'^login$', LoginView.as_view(), name='login'),
    re_path(r'^f_login$', FingerprintLoginView.as_view(), name='f_login'),
    re_path(r'^logout$', LogoutView.as_view(), name='logout'),
    re_path(r'^userinfo$', UserInfoView.as_view(), name='userinfo'),
    re_path(r'^refresh$', RefreshTokenView.as_view(), name='refresh'),
    re_path(r'^qrdrive$', AliyunDriveQRView.as_view(), name='qrdrive'),
    re_path(r'^upload$', AliyunDriveUploadView.as_view(), name='upload'),
    re_path(r'^many/(?P<name>\w+)$', ManyView.as_view(), name='many'),
    re_path('', include(router.urls))
]
