# -*- coding: utf-8 -*-
from datetime import datetime
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.text import truncate_words
from django.contrib.contenttypes.models import ContentType
from models import PostingWall, Posting

class PostingForm(forms.Form):
    content_type = forms.IntegerField()
    object_id = forms.IntegerField()
    post = forms.CharField()
    
    def save(self, user, *args, **kwargs):
        # get wall, check if it exists
        ctype = ContentType.objects.get(pk=self.cleaned_data["content_type"])
        object = ctype.get_object_for_this_type(pk=self.cleaned_data["object_id"])
        wall = PostingWall.objects.filter(content_type=ctype, object_id=object.pk)
        if not wall:
            wall = PostingWall.objects.create(content_type=ctype, object_id=object.pk)
        else:
            wall = wall[0]
            
        # create posting on the wall
        posting = Posting.objects.create(creator=user, posting_wall=wall,
                               body=self.cleaned_data["post"])
        return posting