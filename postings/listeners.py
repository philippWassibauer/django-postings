from models import Posting 
from django.contrib.comments.signals import comment_was_posted
from django.contrib.comments.models import Comment
from django.db.models.signals import post_save, pre_delete, m2m_changed
from django.contrib.auth.models import User
from django.conf import settings

notification = None
if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
    
def new_comment(handler=None, instance=None, created=False, **kwargs):
    if notification:
        # check if the new comment was posted on a Posting
        if created:
            if isinstance(instance.content_object, Posting):
                posting_creator = instance.content_object.creator
                # only send notification to the creator if comment was not posted by himself
                if posting_creator != instance.user:
                    notification.send([posting_creator], "posting_commented",
                                    {"posting": instance.content_object,
                                     "comment": instance})
                    
                # now check who else has posted comments if the creator of post or comment is in list then remove
                user_ids = Comment.objects.for_model(instance.content_object)\
                                                .exclude(user__in=[posting_creator, instance.user])\
                                                .values_list('user', flat=True).distinct()
                
                users = User.objects.filter(pk__in=user_ids)
                
                if users:
                    notification.send(users, "posting_also_commented",
                                        {"posting": instance.content_object,
                                         "comment": instance})
            
            
def start_listening():
    post_save.connect(new_comment, sender=Comment, dispatch_uid="posting.got.commented")
   