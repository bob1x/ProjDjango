from django.db import models
from django.db.models.constraints import UniqueConstraint
from django.contrib.auth.models import AbstractUser, Group, Permission
from datetime import datetime, timezone

#to create migration files
#python manage.py makemigrations

#to migrate migration files
#python manage.py migrate

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class User(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='user_photos', null=True, blank=True)
    telnum = models.CharField(max_length=8, default='00000000' ,null=True)
    friends = models.ManyToManyField("User", related_name='user_friends',blank=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.email}"
    
    # def send_friend_request(self, user):
    #     if not FriendRequest.objects.filter(from_user=self, to_user=user).exists():
    #         FriendRequest.objects.create(from_user=self, to_user=user)
    #         Notification.objects.create(
    #             sender=self,
    #             recipient=user,
    #             notification_type='friend_request',
    #             message=f'{self.first_name} {self.last_name} sent you a friend request.'
    #         )

    # def accept_friend_request(self, friend_request):
    #     if friend_request.to_user == self and not friend_request.is_accepted:
    #         friend_request.is_accepted = True
    #         friend_request.save()
    #         self.friends.add(friend_request.from_user)
    #         friend_request.from_user.friends.add(self)
    #         Notification.objects.create(
    #             sender=self,
    #             recipient=friend_request.from_user,
    #             notification_type='friend_request',
    #             message=f'{self.first_name} {self.last_name} accepted your friend request.'
    #         )

    # def reject_friend_request(self, friend_request):
    #     if friend_request.to_user == self:
    #         friend_request.delete()

class FriendRequest(models.Model):
    from_user = models.ForeignKey(
        User,related_name='from_user',on_delete=models.CASCADE)
    to_user = models.ForeignKey(
        User , related_name='to_user',on_delete=models.CASCADE)
    
    is_accepted = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.from_user} -> {self.to_user}'
        
    
    


# Poste Models
class Poste(models.Model):
    image = models.ImageField(blank=True,upload_to='post_photos')
    POST_TYPE_CHOICES = (
        (0, "Offre"),
        (1, "Demande"),
    )
    poste_type = models.IntegerField(choices=POST_TYPE_CHOICES)
    date_upload = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poste_field = models.CharField(max_length=255 ,default='')
    likes = models.IntegerField(default=0)
    
   
    
    def user_has_liked(self, user):
        return Likes.objects.filter(user=user, poste=self).exists()

    def __str__(self):
        return f"{self.user.email}- {self.date_upload} {self.image} {self.poste_field} {self.likes}"


class Recommandation(Poste):
    texte = models.CharField(max_length=255)


class Transport(Poste):
    depart = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    # add date field
    heure_dep = models.TimeField()
    nbre_sieges = models.IntegerField()
    contact_Trans = models.CharField(max_length=255)


class Logement(Poste):
    localisation = models.CharField(max_length=255)
    description = models.TextField()
    logment_contact = models.CharField(max_length=255)


class Stage(Poste):
    typeStg = models.IntegerField(
        choices=[
            (1, "Ouvrier"),
            (2, "Technicien"),
            (3, "PFE"),
        ]
    )
    societe = models.CharField(max_length=255)
    duree = models.IntegerField()
    sujet = models.CharField(max_length=255)
    contact_Stage = models.CharField(max_length=255)
    specialite = models.CharField(
        max_length=5,
        choices=[
            ("IT", "IT - Technologie informatique"),
            ("SEG", "SEG - Sc Eco et Gestion"),
            ("GC", "GC - Génie Civil"),
            ("GP", "GP - Génie des Procédés"),
            ("GM", "GM - Génie Mécanique"),
        ],
    )



    

class Comment(models.Model):
    poste = models.ForeignKey(Poste, on_delete=models.CASCADE, related_name="comment")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    
def __str__(self):
        return f'Comment by {self.user.email} on {self.post.poste_field}'

class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poste = models.ForeignKey(Poste, on_delete=models.CASCADE, related_name="post_likes")
    


class Intrested(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey('Evenement', on_delete=models.CASCADE ,related_name="event_intrest")
    

# Evenement classes :
class Evenement(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    place = models.CharField(max_length=255)
    contact_Event = models.CharField(max_length=255)
    date_enev = models.DateField()
    heure_deb = models.TimeField()
    heure_fin = models.TimeField()
    place_dispo = models.IntegerField()
    img = models.ImageField(blank=True ,upload_to='event_photos')
    price = models.FloatField(default=0.0)
    interest = models.IntegerField(default=0)
 
    def __str__(self):
       return f"{self.title + self.description }" 
   
    
    

class Archives(models.Model):
    event = models.OneToOneField(Evenement, on_delete=models.CASCADE)
    reason = models.TextField()
    archived_at = models.DateTimeField(auto_now_add=True)
    archived_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='archived_events')
  

    

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('intrested', 'Intrested'),
        ('friend_request', 'friend request')
        # Add other notification types if needed
    )

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True) # type: ignore
    is_read = models.BooleanField(default=False)
    friend_request = models.ForeignKey(FriendRequest, on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return f'{self.sender} {self.notification_type} {self.recipient}'
    
    

class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name='conversations')
   
    @property
    def messages(self):
        return self.messages.all()
    
class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
