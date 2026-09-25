from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
  class Role(models.TextChoices):
    SYSTEM_ADMIN = "SYSTEM_ADMIN", "System Admin"
    OWNER = "OWNER", "Owner"
    MANAGER = "MANAGER", "Manager"

  email = models.EmailField(unique=True)
  first_name = models.CharField(max_length=150, blank=False)
  middle_name = models.CharField(max_length=150, blank=True)
  last_name = models.CharField(max_length=150, blank=False)

  role = models.CharField(
      max_length=20,
      choices=Role.choices,
      default=Role.MANAGER,
  )
  updated_at = models.DateTimeField(auto_now=True)

  REQUIRED_FIELDS = ["email", "first_name", "last_name"]

  @property
  def full_name(self):
    if self.middle_name:
      return f"{self.first_name} {self.middle_name} {self.last_name}"
    return f"{self.first_name} {self.last_name}"

  @property
  def is_system_admin(self):
    return self.role == self.Role.SYSTEM_ADMIN

  @property
  def is_owner(self):
    return self.role == self.Role.OWNER

  @property
  def is_manager(self):
    return self.role == self.Role.MANAGER