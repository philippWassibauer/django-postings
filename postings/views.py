from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponsePermanentRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import date_based
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from models import Posting, PostingWall
from forms import PostingForm


def load_postings(request, id, template_name="postings/posting_list.html"):
    wall = get_object_or_404(PostingWall, pk=id)
    last_posting = int(request.GET.get("last_posting"))
    postings = wall.postings.filter(pk__lt=last_posting)[0:20]
    return render_to_response(template_name,{
        "postings": list(postings),
        "wall": wall,
    }, context_instance=RequestContext(request))
    
    
@login_required
def post(request):
    if request.POST:
        form = PostingForm(request.POST)
        if form.is_valid():
            posting = form.save(request.user)
            return render_to_response("postings/posting_form_reply.html",{
                "posting": posting,
                "content_type": form.cleaned_data["content_type"],
                "object_id": form.cleaned_data["object_id"],
            }, context_instance=RequestContext(request))
        else:
            return HttpResponse(status=400, content="Form was not valid")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
    
    
@login_required   
def posting(request, id):
    posting = get_object_or_404(Posting, pk=id)
    return render_to_response("postings/posting.html",{
        "posting": posting,
    }, context_instance=RequestContext(request))
    
@login_required
def delete(request, id):
    posting = get_object_or_404(Posting, pk=id)
    if request.method == "POST":
        if posting.creator == request.user:
            posting.delete()
            return HttpResponse(status=200, content="OK")
    return HttpResponse(status=400, content="Not allowed")
    
    