from django.contrib import admin

from .models import *


class RedHackWeekAdmin(admin.ModelAdmin):
    list_display    = ['title', 'status', 'start', 'end']
    prepopulated_fields = {'slug': ('title',)}



class IdeaAdmin(admin.ModelAdmin):
    list_display    = ['title']
    prepopulated_fields = {'slug': ('title',)}



admin.site.register(Idea,           IdeaAdmin)
admin.site.register(RedHackWeek,    RedHackWeekAdmin)
admin.site.register(Project)

