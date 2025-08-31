from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # extend later if needed
    pass

class Organization(models.Model):
    id = models.UUIDField(primary_key=True, default=..., editable=False)
    name = models.CharField(max_length=200, unique=True)

class Membership(models.Model):
    ORG_ROLES = [("owner","Owner"),("admin","Admin"),("member","Member"),("viewer","Viewer")]
    org = models.ForeignKey(Organization, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(choices=ORG_ROLES, max_length=16)
    class Meta:
        unique_together = [("org","user")]

class Collection(models.Model):
    """A document bucket inside an org (e.g., Project Alpha)."""
    org = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    class Meta:
        unique_together = [("org","name")]
