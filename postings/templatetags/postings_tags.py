from django.template import Variable, Library, Node, TemplateSyntaxError, TemplateDoesNotExist
from django.template.loader import render_to_string
from django.contrib.contenttypes.models import ContentType

register = Library()


@register.inclusion_tag("postings/posting_form.html")
def posting_form(object):
    # check if following already
    ctype = ContentType.objects.get_for_model(object)
    return {"content_type": ctype.pk, "object_id":object.pk}


@register.inclusion_tag("postings/share.html")
def posting_share(object):
    ctype = ContentType.objects.get_for_model(object)
    return {"content_type": ctype.pk, "object_id":object.pk}