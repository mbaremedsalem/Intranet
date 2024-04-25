from django.contrib import admin
from django.contrib.auth.hashers import make_password
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import *

# Register your models here.

admin.site.site_header = "Intranet"

class UserAdminConfig(admin.ModelAdmin):
    model = UserAub
    search_fields = ('email','nom', 'phone','prenom','post','image','username')
    list_filter = ('email', 'nom', 'phone','post','image','is_active', 'is_staff','username')
    ordering = ('nom',)  # Update the ordering field here
    list_display = ('phone','email', 'nom', 'post','image','prenom','username','role','is_superuser',
                    'is_active', 'is_staff', 'is_blocked', 'password',)
    fieldsets = (
        (None, {'fields': ('email', 'nom','post','image','prenom','username','phone','role',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_blocked')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nom','post','image','prenom','phone','username','is_active', 'is_staff', 'is_blocked')
            }
         ),
    )


class AdminResource(resources.ModelResource):
    class Meta:
        model = Admin
        fields = ('email', 'nom', 'prenom', 'post', 'direction', 'phone', 'username', 'password', 'role','is_active', 'is_staff', 'is_blocked')
        import_id_fields = []  # Ignorer le champ "id" lors de l'importation

    def before_export(self, queryset, *args, **kwargs):
        # Hasher le mot de passe de chaque objet avant l'exportation
        for obj in queryset:
            if obj.password:
                obj.password = make_password(obj.password)


class UserAdmin(ImportExportModelAdmin):
    model = Admin
    resource_class = AdminResource
    search_fields = ('email', 'nom','post','phone','prenom','direction','username')
    list_filter = ('email', 'nom', 'post','phone','direction' ,'is_active', 'is_staff')
    ordering = ('nom',)  # Update the ordering field here
    list_display = ('phone','prenom','post','email','direction','username','nom','is_superuser',
                    'is_active', 'is_staff', 'is_blocked', 'password',)
    fieldsets = (
        (None, {'fields': ('email', 'nom','post','direction','username','phone','image','role','prenom')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_blocked')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nom','direction' ,'post','prenom','username','phone','is_active', 'is_staff', 'is_blocked')
            }
         ),
    )  

    def save_model(self, request, obj, form, change):
        # Hasher le mot de passe uniquement s'il est présent et qu'il a été modifié
        if obj.password:
            obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)


class UserAgent(admin.ModelAdmin):
    model = Agent
    search_fields = ('email', 'nom','post','phone','prenom','direction','username')
    list_filter = ('email', 'nom', 'post','phone','direction' ,'is_active', 'is_staff')
    ordering = ('nom',)  # Update the ordering field here
    list_display = ('phone','prenom','post','email','direction','username','nom','is_superuser',
                    'is_active', 'is_staff', 'is_blocked', 'password',)
    fieldsets = (
        (None, {'fields': ('email', 'nom','post','direction','username','phone','image','role','prenom')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_blocked')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nom','direction' ,'post','prenom','username','phone','is_active', 'is_staff', 'is_blocked')
            }
         ),
    )  

class DocumentConf(admin.ModelAdmin):
    model = Documents
    search_fields = ('sujet', 'code','description','file','direction','date_ajout')
    list_filter = ('sujet', 'code','description','file','direction','date_ajout')
    ordering = ('sujet',)  # Update the ordering field here
    list_display = ('sujet', 'code','description','file','direction','date_ajout')
    fieldsets = (
        (None, {'fields': ('sujet','description','file','direction',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('sujet','description','file','direction','date_ajout','user')
            }
         ),
    )

class DirectionConf(admin.ModelAdmin):
    model = Direction
    search_fields = ('nom','code')
    list_filter = ('nom','code')
    ordering = ('nom',)  # Update the ordering field here
    list_display = ('nom','code')
    fieldsets = (
        (None, {'fields': ('nom','code')}),
        
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('nom','code')
            }
         ),
    ) 

class ArchiveConf(admin.ModelAdmin):
    model = Archive
    search_fields = ('nom','date_ajout')
    list_filter = ('nom','date_ajout')
    ordering = ('nom',)  # Update the ordering field here
    list_display = ('nom','date_ajout')
    fieldsets = (
        (None, {'fields': ('nom','date_ajout')}),
        
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('nom','date_ajout')
            }
         ),
    ) 

           

admin.site.register(UserAub, UserAdminConfig)
admin.site.register(Agent, UserAgent)

admin.site.register(Admin, UserAdmin)
admin.site.register(Documents,DocumentConf)
admin.site.register(Direction,DirectionConf)
# admin.site.register(Archive)
admin.site.register(Avis)
admin.site.register(procedur)
admin.site.register(note)
admin.site.register(decision)
admin.site.register(charts)
admin.site.register(plotique)

# {
# 	"Version": "2012-10-17",
# 	"Statement": [
# 		{
# 			"Effect": "Allow",
# 			"Principal": "*",
# 			"Action": "s3:ListBucket",
# 			"Resource": "arn:aws:s3:::shop-django-rest"
# 		},
# 		{
# 			"Effect": "Allow",
# 			"Principal": "*",
# 			"Action": "s3:GetBucketLocation",
# 			"Resource": "arn:aws:s3:::shop-django-rest"
# 		},
# 		{
# 			"Effect": "Allow",
# 			"Principal": "*",
# 			"Action": [
# 				"s3:GetObject",
# 				"s3:DeleteObject"
# 			],
# 			"Resource": "arn:aws:s3:::shop-django-rest/*"
# 		}
# 	]
# }






