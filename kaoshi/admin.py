from django.contrib import admin
from kaoshi.models import Select, Selects, Judge, Bugs, UserInfo
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
# Register your models here.

@admin.register(Select)
class SelectAdmin(admin.ModelAdmin):
    list_display = ["id", "topic", "key"]

@admin.register(Selects)
class SelectsAdmin(admin.ModelAdmin):
    list_display = ["id", "topic", "key"]

@admin.register(Judge)
class JudgeAdmin(admin.ModelAdmin):
    list_display = ["id", "topic", "key"]

@admin.register(Bugs)
class BugsAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "date", "content"]

class EmployeeInline(admin.StackedInline):
    model = UserInfo
    can_delete = False
    verbose_name_plural = 'employee'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (EmployeeInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['user', 'fraction']