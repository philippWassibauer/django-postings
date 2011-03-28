from django.template import Variable, Library, Node, TemplateSyntaxError, TemplateDoesNotExist
from django.template.loader import render_to_string
from django.contrib.contenttypes.models import ContentType
from postings.models import PostingWall

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
    
    
@register.inclusion_tag("postings/postings.html")
def object_postings(object, user, offset=0, count=10):
    wall = PostingWall.objects.get_wall_of_object(object)
    
    #create one if it does not exist
    if not wall:
        wall = PostingWall(postings_on=object)
        wall.save()
        
    return wall_postings(wall, user,
                         offset, count)

@register.inclusion_tag("postings/postings.html")
def wall_postings(wall, user, offset=0, count=10):
    return {"postings": wall.postings.all()[offset:count],
            "user": user,
            "wall": wall}