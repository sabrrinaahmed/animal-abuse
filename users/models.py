from django.db import models
from PIL import Image
from django.contrib.auth import get_user_model
from allauth.account.signals import user_signed_up, user_logged_in


User = get_user_model()

# Create your models here.
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	image = models.ImageField(null = True, default='default.jpg', upload_to = 'profile_pics')

	def __str__(self):
		return f'{self.user.username} Profile'

	def save(self, *args, **kwargs):
		super(Profile, self).save(*args,**kwargs)

		img = Image.open(self.image.path)

		if img.height > 300 or img.width > 300:
			output_size = (300, 300)

			img.thumbnail(output_size)
			img.save(self.image.path)


def user_profile(request, user, **kwargs):
	if user_signed_up:
		Profile.objects.create(user=user)
		print(user)

user_signed_up.connect(receiver=user_profile, sender=User)