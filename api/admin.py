from django.contrib import admin
from .models import UserAub,Agent,Girant,Documents,Direction
# Register your models here.

admin.site.site_header = "Intranet"

class UserAdminConfig(admin.ModelAdmin):
    model = UserAub
    search_fields = ('email','nom', 'phone','prenom',)
    list_filter = ('email', 'nom', 'phone', 'is_active', 'is_staff')
    ordering = ('nom',)  # Update the ordering field here
    list_display = ('phone','email', 'nom', 'prenom','role','is_superuser',
                    'is_active', 'is_staff', 'is_blocked', 'password',)
    fieldsets = (
        (None, {'fields': ('email', 'nom', 'prenom','phone','role',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_blocked')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nom','prenom','phone', 'is_active', 'is_staff', 'is_blocked')
            }
         ),
    )

class UserGirant(admin.ModelAdmin):
    model = Girant
    search_fields = ('email', 'nom', 'phone','prenom',)
    list_filter = ('email', 'nom', 'phone', 'is_active', 'is_staff')
    ordering = ('nom',)  # Update the ordering field here
    list_display = ('phone','prenom','email', 'nom', 'is_superuser',
                    'is_active', 'is_staff', 'is_blocked', 'password',)
    fieldsets = (
        (None, {'fields': ('email', 'nom', 'phone','image','role','prenom')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_blocked')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nom', 'prenom','phone', 'is_active', 'is_staff', 'is_blocked')
            }
         ),
    )

class UserAgent(admin.ModelAdmin):
    model = Agent
    search_fields = ('email', 'nom', 'phone','prenom','direction')
    list_filter = ('email', 'nom', 'phone','direction' ,'is_active', 'is_staff')
    ordering = ('nom',)  # Update the ordering field here
    list_display = ('phone','prenom','email','direction' ,'nom', 'is_superuser',
                    'is_active', 'is_staff', 'is_blocked', 'password',)
    fieldsets = (
        (None, {'fields': ('email', 'nom','direction' ,'phone','image','role','prenom')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_blocked')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nom','direction' ,'prenom','phone', 'is_active', 'is_staff', 'is_blocked')
            }
         ),
    )    

admin.site.register(UserAub, UserAdminConfig)
admin.site.register(Agent, UserAgent)
admin.site.register(Girant, UserGirant)
admin.site.register(Documents)
admin.site.register(Direction)

