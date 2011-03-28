from datetime import datetime, timedelta

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import truncatewords
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

    
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
    posting_wall= models.ForeignKey('PostingWall', related_name="postings")
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


from listeners import start_listening
start_listening()
