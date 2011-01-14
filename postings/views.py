from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, Http404, HttpResponsePermanentRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import date_based
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from models import Posting, PostingWall

def post(request):
    if request.POST:
        # get wall, check if it exists
        ctype = ContentType.objects.get(pk=request.POST.get("content_type"))
        object = ctype.get_object_for_this_type(pk=request.POST.get("object_id"))
        wall = PostingWall.objects.filter(content_type=ctype, object_id=object.pk)
        if not wall:
            wall = PostingWall.objects.create(content_type=ctype, object_id=object.pk)
        else:
            wall = wall[0]
            
        # create posting on the wall
        posting = Posting.objects.create(creator=request.user, posting_wall=wall,
                               body=request.POST.get("post"))
        
        attachment = []
        if "attachments" in settings.INSTALLED_APPS:
            from attachments.models import add_attachment
            attachment = add_attachment(posting, request.POST.get("attachment_id"))
            
        return render_to_response("postings/posting_form_reply.html",{
            "posting": posting,
            "content_type": ctype,
            "object_id": posting.pk,
        }, context_instance=RequestContext(request))
        
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))