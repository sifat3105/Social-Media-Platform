from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name= 'profile')
    image = models.ImageField(upload_to='profile_pics/', default='default.jpg')
    date_of_barth= models.DateField( auto_now=False, auto_now_add=False, blank=True, null=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    friends = models.ManyToManyField('self', symmetrical=True, blank=True)
    two_step_auth = models.BooleanField(default= False)
    
    def __str__(self):
        return self.user.username

    def add_friend(self, profile):
        """ Add a friend to the profile's friends list. """
        self.friends.add(profile)

    def remove_friend(self, profile):
        """ Remove a friend from the profile's friends list. """
        self.friends.remove(profile)
    
    def is_friend(self, profile):
        """ Check if the given profile is a friend. """
        return self.friends.filter(id=profile.id).exists()
