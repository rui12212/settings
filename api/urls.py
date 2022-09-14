from django.urls import path, include#PathとIncludeのインポート。無いと使えないから！
from . import views#同じ階層にあるViewsをImport
from rest_framework.routers import DefaultRouter

app_name = 'user'
#RouterでViewとURLSを紐付けるその場合、下記から始める

router = DefaultRouter()
#ここにregisterというメソッドを使用し、ViewとPathのセットをどんどん追加していく
router.register('profile', views.ProfileViewSet)#profileとviews(viewsのProfileViewSet）を紐付け
#Routerが紐付けっれるのは、ModelViewSetのみ！Views.pyでModelViewSetで引数をしていしていたもののい下記で紐付け
router.register('post', views.PostViewSet)#ちなみに、''の中に入っているのはPATH名
router.register('comment', views.CommentViewSet)

#次に、Genericsの汎用Viewを引数としていたものは、下記で紐付け

urlpatterns = [
    path('register/', views.CreateUserView.as_view(), name='register'),#一番左のやつはURLが同表示されるか、 as.View()はつける決まり、一番右はPATHの名前
    #上記で、register/にアクセスすると、CreateUserViewにアクセスできる
    path('myprofile/', views.MyProfileListView.as_view(), name='myprofile'),#ログインしているUserのProfile情報を返してくれるView
    #apiのPATHに来たときに、Routerを読むように指示するのがした
    path('', include(router.urls)),
]
#ここまで来たら、このURLS．Pyをapi_insta（親のURLｓ．ｐｙ）と紐付けを行う。親、プロジェクト側のURLS.pyに移動



