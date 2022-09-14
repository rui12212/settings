#admin画面で管理ができるようにするため
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from . import models
#adminと同じ階層にあるmodelsをimport(自由にmodelsのclassが使えるようになる)

class UserAdmin(BaseUserAdmin):#ここの表記は、Adminの中で解説。Adminの管理画面での表示を指示。
    ordering = ['id']
    list_display = ['email']#Emailの表示
    fieldsets = (
        (None,{'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields':()}),
        (
            _('permissions'),
            {
                'fields':(
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )
admin.site.register(models.User, UserAdmin) #この一文は決まり、models.UserとUserAdminを入れる約束
admin.site.register(models.Comment)
admin.site.register(models.Profile)#models.名前でDjangoにModel構造を登録できる
admin.site.register(models.Post)

#今回のようにUserをOverwriteしているときは、ModelのClassUsrAdminをmodelsに貼り付ける必要がある(#¢#でサインしている）

#上記全部書き終わったっら、次はUrl.pyの編集。どのURLをに上記の情報が載るかがわからないため。
#ここまで終わったらAdminに入るために、Superuserを一つ設定する
#その後はSeliarizerの新規ファイルを作成する

# Register your models here.
