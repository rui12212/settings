
#一番最初のコメントは削除して良い
from django.contrib import admin
from django.urls import path, include#Patthとincludeの追加
#アプリ側のURLS.pyが終わったら、下記を追記
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),#ここにアクセスするとAdminに入れる。ここが一番親のURL。アプリごとにURLを作って親のところに紐付ける必要がある
    path('api/', include('api.urls')),#アプリ側のURLS.pyに紐付け。これでアプリ側のURLの5つのPATHにアクセスできる
    #api/とURLを打てば、アプリ側のURLS．ｐｙにいける。例えば、api/profileなど
    path('authen/', include('djoser.urls.jwt')),#Djoserを使う時に必要。authen/jwt/createでアクセスし、EmailとNameをPOSTするとJWTを返す仕組み
]

#最後に、mediaフォルダの直下に格納されるAvatar情報にアクセスするためのURLを設定
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#settings.pyの一番最後で、MEDIA_ROOTとMEDIA_URLをどちらも/media/で登録している
#MediaというURLを入力すると、Document.rootを使って、PJ内のMediaファイルを見に行く。そしてリンクも形成してURLPatternsの中に入れることも指示
#この一文により、画像URLをクリックすると画像が表示できるようになっている

#ここまで来たら、API_Endpointがしっかりできているか動作確認