from django.urls import include, re_path
from rest_framework.routers import SimpleRouter

from api.views.action import ManyActionView
from api.views.aliyundrive import AliyunDriveQRView, AliyunDriveView
from api.views.auth import LoginView, LogoutView, UserInfoView, RefreshTokenView, FingerprintLoginView
from api.views.book import BookInfoView, BookLabelInfoView
from api.views.download import DownloadView
from api.views.files import FileInfoView
from api.views.lobby import BookLobbyView, BookCategoryView, LobbyAction, BookDetailView, BookRankDataView, \
    BookCategoriesView
from api.views.upload import AliyunDriveUploadView, UploadView

router = SimpleRouter(False)
router.register('drive', AliyunDriveView)
router.register('file', FileInfoView)
router.register('book', BookInfoView)
router.register('detail', BookDetailView)
router.register('download', DownloadView)
router.register('category', BookCategoryView)
urlpatterns = [
    re_path(r'^login$', LoginView.as_view(), name='login'),
    re_path(r'^f_login$', FingerprintLoginView.as_view(), name='f_login'),
    re_path(r'^logout$', LogoutView.as_view(), name='logout'),
    re_path(r'^userinfo$', UserInfoView.as_view(), name='userinfo'),
    re_path(r'^refresh$', RefreshTokenView.as_view(), name='refresh'),
    re_path(r'^qrdrive$', AliyunDriveQRView.as_view(), name='qr_drive'),
    re_path(r'^upload$', AliyunDriveUploadView.as_view(), name='upload'),
    re_path(r'^upload/file$', UploadView.as_view(), name='upload_file'),
    re_path(r'^label$', BookLabelInfoView.as_view(), name='book_label'),
    re_path(r'^lobby$', BookLobbyView.as_view(), name='lobby'),
    re_path(r'^categories$', BookCategoriesView.as_view(), name='categories'),
    re_path(r'^rank$', BookRankDataView.as_view(), name='rank'),
    re_path(r'^action$', LobbyAction.as_view(), name='lobby_action'),
    re_path(r'^many/(?P<name>\w+)$', ManyActionView.as_view(), name='many_action'),
    re_path('', include(router.urls))
]
