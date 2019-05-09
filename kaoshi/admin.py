from django.contrib import admin
from kaoshi.models import Select, Selects, Judge, Bugs
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