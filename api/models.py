from django.db import models

# Create your models here.
#Userの作成
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings

#ProfileのPathのさくせい
def upload_avatar_path(instance, filename):#Profilの引数をInstanceとし、ユーザーが設定したファイルNameをそのまま受け取るよう指示
    ext = filename.split('.')[-1]#Extは拡張子を入れる箱。Filenameをドットで区切った時の後ろから最初の1番目を指定
    return '/'.join(['avatars', str(instance.userProfile.id)+str(instance.nickName)+str(".")+str(ext)])#JoinでAvatarというフォルダを作り、その中に、UsrProfiineのId、Nickname、拡張子（Ext）をつけて、Avatarファイルの直下においている。


#PostのPath作成
def upload_post_path(instance, filename):
    ext=filename.split('.')[-1]
    return '/'.join(['posts', str(instance.userPost.id)+str(instance.title)+str(".")+str(ext)])#Postの直下にファイルが溜まるように設定


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):#通常はUserNameであるのをemail用にカスタマイズするために再定義している
       #ログイン画面のパスワードemail認証。django搭載のClassを呼び出して、それをemailに書き出す
        if not email:
            raise ValueError('email is must')#エラーを出す

        user=self.model(email=self.normalize_email(email))#モデルメッソ度を使い、Userインスタンスを作成→正規化（大文字を小文字にならす）
        user.set_password(password)#そのインスタンスに対してPasswordを設定。パスワードのハッシュ化をそている
        user.save(using=self._db)#作ったUSえｒをセーブする処理

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)#通常のUsserを作る、そのあとソタの3行で権限の付与をしている
        user.is_staff = True#Staff権限の付与
        user.is_superuser = True#Suprtuserの権限付与
        user.save(using= self._db)#入力したUserのSaveを行う

        return user

class User(AbstractBaseUser, PermissionsMixin):#djangoｎデフォルトではいいている、"User"をEmail用にオーバーライドしている

    email = models.EmailField(max_length=50, unique=True)#modelsのEmailFieldにアクセスしている。unique=Trueは重複したメールアドレスを認めない
    is_active = models.BooleanField(default=True)#全てのUserにactiveの権限は与えるが
    is_staff = models.BooleanField(default=False)#Adminにアクセスする権限は与えない

    objects = UserManager()#上記UserManagerのクラスのインスタンスをObjectに入れている。Classの中にさらにClassが入っている。これにより、「object.create_user」とすることで、create_userのMethodを、Userのインスタんっすから呼ぶことができる

    USERNAME_FIELD = 'email'#デフォルトはUsername

    def __str__(self):
        return self.email#Email内容を文字列で返してくれる関数。

#Profileの作成→次はPost
class Profile(models.Model):#Profileを格納するClass
    nickName = models.CharField(max_length=20)#　models.CharFieldで文字数を設定
    userProfile = models.OneToOneField(#DjangoのUseerモデルとUserprofileをOnetoOneFieldで紐付ける
        settings.AUTH_USER_MODEL, related_name='userProfile',
        on_delete=models.CASCADE# userProfileを消した時、OnetoOneFieldで結びついたProfileも消去される
    )
    created_one = models.DateTimeField(auto_now_add=True)#自動で日時を入れてくれる
    img = models.ImageField(blank=True, null=True, upload_to=upload_avatar_path)#Upload＿Toでイメージを保存するPathを指定できる。これから別でUpload_Avatar_pathの関数を作らないといけない（UserManagerの上に作ってるやつ）

    def __str__(self):
        return self.nickName

#Postの作成

class Post(models.Model):
    title = models.CharField(max_length=100)
    userPost = models.ForeignKey(#どの記事をどのUserが投稿したかをわかるようにするため）
        settings.AUTH_USER_MODEL, related_name='userPost',#ForeignkeyでDjangoのUserモデルを紐付けている。
        on_delete=models.CASCADE
    )
    created_on = models.DateTimeField(auto_now_add=True)#データが入れられた日時を自動で取得
    img=models.ImageField(blank=True, null=True, upload_to=upload_post_path)
    liked=models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='linked', blank=True)#投稿とUserの関係がManyToManyのため

    def __str__(self):
        return self.title

#Commentの作成

class Comment(models.Model):
    text=models.CharField(max_length=100)
    userComment=models.ForeignKey(#誰がコメントしたかをわかるように、ForeignkeyでUser名を紐付けしている
        settings.AUTH_USER_MODEL, related_name='userComment',
        on_delete=models.CASCADE
    )
    post=models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.text