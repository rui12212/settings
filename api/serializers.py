from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Profile, Post, Comment

#serializerはModelsで定義したモデル（Classs）ごとに一つ一つ作っていこう

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'password')
        extra_kwargs= {'password': {'write_only':True}}#extra_kwargsでWrite_onlyなど指定できる。

    def create(self, validated_date):#CreateMethoddの上書き。昨日は、Userの作成と新しくユーザーを作成した時の表示方法の指示

        user = get_user_model().objects.create_user(**validated_date)#Userは、Models.pyで指定した情報（40-50）を受け取り、データがValidであれば、それを
        return user

#次はProfileManagerの設定（投稿者・読んでいる人の識別）

class ProfileSerializer(serializers.ModelSerializer):
    created_on = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)#既存のDate表示だとめちゃくちゃ長いから、省略のための機能追加

    class Meta:
        model = Profile#ProfileModelという既存のModelを使用
        fields = ('id', 'nickName', 'userProfile', 'created_on', 'img')#mModelsと名前が一致していないとうまく行かない。Profile作成時にここの値が帰ってくるため
        extra_kwargs = {'userProfile':{'read_only':True}}#UserProfileにはログインしているUserが入る。ただ書き込むときにClient側で毎回User情報を入れるのは辛いから、Django側で自動でログイン中の人のProfileを取得するヨウ、後ほどVews.pyで編集予定

#次はPostModelのしリアライザー作成（投稿時）

class PostSerializer(serializers.ModelSerializer):
    created_on = serializers.DateTimeField(format='%Y-%m-%d', read_only=True)
    class Meta:
        model = Post
        fields = ('id', 'title', 'userPost', 'created_on', 'img', 'linked')
        extra_kwargs = {'userPost':{'read_only': True}}

#コメントをする人の設定

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'title', 'userComment', 'post')
        extra_kwargs = {'userComment':{'read_only':True}}

#ここまでおわったらViewの編集に入る

