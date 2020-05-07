from django.contrib.auth.models import User

class UserProfile(models.Model):
    user   = models.OneToOneField(User)
    avatar = models.ImageField()