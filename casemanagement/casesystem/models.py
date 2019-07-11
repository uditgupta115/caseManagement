from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.management.utils import get_random_secret_key
from django.db import models

from casemanagement.casesystem.managers import UserManager


class Status:
    OPEN = 1
    RESOLVED = 2
    REOPENED = 3
    CLOSED = 4


STATUS_CHOICES = (
        (None, "Please select status"),
        (Status.OPEN, "Open"),
        (Status.RESOLVED, "Resolved"),
        (Status.REOPENED, "Reopened"),
        (Status.CLOSED, "Closed"),
    )


class Roles:
    MANAGER = 1
    TASK_MANAGER = 2


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(
        max_length=128, blank=True, null=True, default=''
    )
    middle_name = models.CharField(
        max_length=128, blank=True, null=True, default=''
    )
    last_name = models.CharField(
        max_length=128, blank=True, null=True, default=''
    )
    email = models.EmailField(max_length=256, null=True, blank=True)
    username = models.CharField(max_length=256, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    token_secret_key = models.CharField(max_length=128, unique=True, default=get_random_secret_key)

    USERNAME_FIELD = 'username'

    objects = UserManager()

    def __str__(self):
        return self.username


class UserRole(models.Model):
    ROLE_CHOICES = (
        (None, "Please select role"),
        (Roles.MANAGER, "Manager"),
        (Roles.TASK_MANAGER, "Task Manager"),
    )
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    role = models.PositiveSmallIntegerField(blank=True, null=True, choices=ROLE_CHOICES)

    class Meta:
        unique_together = ('user', 'role')

    def __str__(self):
        return "%s - %s" % (self.user, self.get_role_display())


class Case(models.Model):
    role = models.ForeignKey(UserRole, on_delete=models.DO_NOTHING)
    case_name = models.CharField(max_length=512, blank=True, null=True)
    case_status = models.PositiveSmallIntegerField(blank=True, null=True, choices=STATUS_CHOICES)
    remarks = models.TextField(null=True, blank=True)

    def __str__(self):
        return "ID: %s " % self.pk + self.case_name


class Task(models.Model):
    case = models.ForeignKey(Case, on_delete=models.DO_NOTHING)
    role = models.ForeignKey(UserRole, on_delete=models.DO_NOTHING, default=None)
    task_name = models.CharField(max_length=256, blank=True, null=True)
    task_status = models.PositiveSmallIntegerField(blank=True, null=True, choices=STATUS_CHOICES)
    remarks = models.TextField(null=True, blank=True)

    def __str__(self):
        return "ID: %s " % self.pk + self.task_name
