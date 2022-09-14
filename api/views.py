from rest_framework import generics#汎用View
from rest_framework import viewsets
from rest_framework.permissions import AllowAny#JWTの設定をしているため、パスワードがないと未練なくなっているが、最初のUse（登録前のUser）は入れるように設定
from . import serializers#同じ階層のSerializerと
from .models import Profile, Post, Comment#Modelsをいんぽーとしている


class CreateUserView(generics.CreateAPIView):#これは新規Userを作成することに特化したView
    serializer_class = serializers.UserSerializer#Serializerに対象となるSerializerを指定する
    permission_classes = (AllowAny,)#新規で入る人はアクセスできないといけないから

class ProfileViewSet(viewsets.ModelViewSet):#新規投稿・更新のひつ王が有るので、ModelViewSetを設定
    queryset = Profile.objects.all()#Profileに入っているデータをすべて取得
    serializer_class = serializers.ProfileSerializer

    def perform_create(self, serializer):#ログインしている人の情報を自動で割り当て、検出する部分の処理。PerfomeCreateはProfileを新規作成するときに呼ばれる
        serializer.save(userProfile=self.request.user)#request.userでは、新規でログインする時のProfiLe情報を抜き取り、UserProfileとして記録すること

class MyProfileListView(generics.ListAPIView):#ログインしているUserのProfileを返してくれる機能
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer#serializer_classで右辺を当て、その下def get_query＿Setを上書きしている
    def get_queryset(self):
        return self.queryset.filter(userProfile=self.request.user)#ログインしているUserだけを返すようにしたい。ため、Filiterをかけて、ログインしているUserと一致しているか判断→一致していれば情報をViewで表示できるようにしている。

#投稿に対するViewを追記

class PostViewSet(viewsets.ModelViewSet):#ModelViewSetの継承
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer#HostSerializerの割当

    def perform_create(self, serializer):
        serializer.save(userPost=self.request.user)#Postするとき、ログインしていいるUserの情報を取得している

#コメントの設定を追記

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer

    def perform_create(self, serializer):
        serializer.save(userComment=self.request.user)#やっていることは上記と同じ

#最後にViewとブラウザから入力するURLのPATHを紐付ける必要がある
#そのため、アプリ内（今はapiフォルダ）の直下にURLS.pyファイルを作成する必要がある→次からURLS.py（アプリ側）を編集