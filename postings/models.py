from datetime import datetime, timedelta

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import truncatewords
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

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
        return 'posting created by %s on %s ( %s )' % ( self.author.username, \
                                  self.created_at, truncatewords(self.body, 9 ))


class PostingWall(models.Model):
    """
    A shared place to post items.
    """
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField() 
    postings_on = generic.GenericForeignKey()
    
    class Meta:
        verbose_name = _('Posting Wall')
        verbose_name_plural = _('Posting Wall')

    def __unicode__(self):
        return "%s's Wall"%self.postings_on