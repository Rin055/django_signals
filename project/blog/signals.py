from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile, Post

    
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=Post)
def increase_post_count(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.get(user=instance.author)
        profile.posts_count += 1
        profile.save()

        print(f"New post created by {instance.author.username}")


@receiver(post_delete, sender=Post)
def decrease_post_count(sender, instance, **kwargs):
    profile = Profile.objects.get(user=instance.author)
    profile.posts_count -= 1
    profile.save()

    print(f"Post deleted: {instance.title}")