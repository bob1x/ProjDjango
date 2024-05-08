from django.db import models
from django.db.models.constraints import UniqueConstraint
from django.contrib.auth.models import AbstractUser, Group, Permission
from datetime import datetime

#to create migration files
#python manage.py makemigrations

#to migrate migration files
#python manage.py migrate

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='user_photos', null=True, blank=True)
    telnum = models.CharField(max_length=8, default='00000000' ,null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.email}"



# Poste Models
class Poste(models.Model):
    image = models.ImageField(blank=True)
    POST_TYPE_CHOICES = (
        (0, "Offre"),
        (1, "Demande"),
    )
    poste_type = models.IntegerField(choices=POST_TYPE_CHOICES)
    date_upload = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True  # Set the model as abstract

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.date_upload} {self.image}"


class Recommandation(Poste):
    texte = models.CharField(max_length=255)


class Transport(Poste):
    depart = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
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


class Reaction(models.Model):
    comment = models.TextField(max_length=999)
    like = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poste = models.ForeignKey(
        Recommandation,
        on_delete=models.CASCADE,
        related_name='reactions',
        null=True
    )
# Evenement classes :
class Evenement(Poste):
    intitule = models.CharField(max_length=255)
    description = models.TextField()
    lieu = models.CharField(max_length=255)
    contact_Event = models.CharField(max_length=255)
    date_enev = models.DateField()
    heure_deb = models.TimeField()
    heure_fin = models.TimeField()
    place_dispo = models.IntegerField()
    


class EvenClub(Evenement):
    club = models.CharField(max_length=255)


class EvenSocial(Evenement):
    prix = models.FloatField()