from django.contrib import admin
from django.contrib.admin.actions import delete_selected

from models import Posting, PostingWall

class PostingWallAdmin(admin.ModelAdmin):
    list_display = ('__unicode__','postings_on')
    actions = [delete_selected,]
    
class PostingAdmin(admin.ModelAdmin):
    list_display = ('__unicode__','posting_wall','creator', 'created_at')
    list_filter = ('posting_wall','creator')
    ordering = ('created_at',)
    actions = [delete_selected,]

admin.site.register(PostingWall, PostingWallAdmin)
admin.site.register(Posting, PostingAdmin)
