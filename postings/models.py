from datetime import datetime, timedelta

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import truncatewords
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

posting_attachment_types = []


def register_posting_attachment(name, modelclass):
    posting_attachment_types.append({"name": name, "modelclass": modelclass})
    
class PostingWallManager(models.Manager):
    def get_wall_of_object(self, object):
        content_type = ContentType.objects.get_for_model(object)
        wall = self.get_query_set().filter(content_type=content_type, \
                                    object_id=object.pk)
        if wall:
            return wall[0]
        else:
            return None

class PostingWall(models.Model):
    """
    A shared place to post items.
    """
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField() 
    postings_on = generic.GenericForeignKey()

    objects = PostingWallManager()

    class Meta:
        verbose_name = _('Posting Wall')
        verbose_name_plural = _('Posting Wall')

    def __unicode__(self):
        return "%s's Wall"%self.postings_on
    
    
class Posting(models.Model):
    """
    A simple note to post on a wall.
    """
    posting_wall= models.ForeignKey('PostingWall')
    creator     = models.ForeignKey(User, related_name="postings")
    body        = models.TextField(_('item_body'))
    created_at  = models.DateTimeField(_('created at'), default=datetime.now)

    class Meta:
        verbose_name        = _('wallitem')
        verbose_name_plural = _('wallitems')
        ordering            = ('-created_at',) 
        get_latest_by       = 'created_at'

    def __unicode__(self):
        return 'posting created by %s on %s ( %s )' % ( self.creator.username, \
                                  self.created_at, truncatewords(self.body, 9 ))


class AbstractPostingAttachment(models.Model):
    """
    An Attachment that can be added to a Post
    """
    posting = models.ForeignKey(Posting)
    
    class Meta:
        abstract = True


def postingimage_get_upload_to(instance, filename):
    year = instance.posting.created_at.year
    return "posting-images/%s/%s/%s"%(instance.posting.creator.pk,
                                      year, filename)
 

IMAGE_UPLOAD = "UPLOAD"
IMAGE_WEBCAM = "WEBCAM"
IMAGE_ATTACHMENT_CHOICES = (
    (IMAGE_UPLOAD, _("upload")),
    (IMAGE_WEBCAM, _("webcam"))
)


class ImageAttachment(AbstractPostingAttachment):
    """
    Attach an Image to a posting
    """
    image = models.ImageField(upload_to=postingimage_get_upload_to,
                              height_field="image_height",
                              width_field="image_width")
    
    image_height = models.IntegerField(editable=False)
    image_width = models.IntegerField(editable=False)
    
    source = models.CharField(editable=False, choices=IMAGE_ATTACHMENT_CHOICES,
                              default=IMAGE_UPLOAD, max_length=40) 
        
register_posting_attachment(_("Image"), ImageAttachment)


class LinkAttachment(AbstractPostingAttachment):
    """
    Attach an Image to a posting
    """
    link = models.CharField(_("Link"), max_length=400)
    
    link_title = models.CharField(_("Link Title"), editable=False, max_length=400,
                                  null=True, blank=True)
    link_description = models.TextField(_("Link Description"), editable=False,
                                        null=True, blank=True)
    
register_posting_attachment(_("Link"), LinkAttachment)


