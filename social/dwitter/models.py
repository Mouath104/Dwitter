from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField(
        "self",
        related_name="followed_by",
        symmetrical=False,
        blank=True
    )
    #new
    img=models.CharField(max_length=40,default='211-2112351_green-twitter-icon.png')
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        user_profile.follows.add(instance.profile)
        user_profile.save()
# Remove: post_save.connect(create_profile, sender=User)

class Dweet(models.Model):

    user = models.ForeignKey(
    User, related_name="dweets", on_delete=models.DO_NOTHING
    )

    body = models.CharField(max_length=140)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
        f"{self.user} "
        f"({self.created_at:%Y-%m-%d %H:%M}): "
        f"{self.body[:30]}..."
        )

class Comment(models.Model):
    user=models.ForeignKey(
        User,
        related_name="comments",
        on_delete=models.CASCADE,
    )
    dweet=models.ForeignKey(
        Dweet,
        related_name="dweets",
        on_delete=models.CASCADE
    )
    body=models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: # new
        indexes = [models.Index(fields=["created_at"])]
        ordering = ["-created_at"]
    def __str__(self):
        return self.user.first_name