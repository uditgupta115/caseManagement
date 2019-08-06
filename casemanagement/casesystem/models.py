from datetime import timedelta, datetime

import jwt
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, AbstractUser
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


class User(AbstractUser):

    token_secret_key = models.CharField(max_length=128, unique=True, default=get_random_secret_key)

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

    @property
    def token(self):
        """
        Allows us to get a user's token by calling `user.token` instead of
        `user.generate_jwt_token().

        The `@property` decorator above makes this possible. `token` is called
        a "dynamic property".
        """
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 60 days into the future.
        """
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'token': self.token_secret_key,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')


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

    def get_all_tasks(self):
        return self.task_set.all()

    def get_all_cases(self):
        return self.case_set.all()


class Case(models.Model):
    role = models.ForeignKey(UserRole, on_delete=models.DO_NOTHING)
    case_name = models.CharField(max_length=512, blank=True, null=True)
    case_status = models.PositiveSmallIntegerField(blank=True, null=True, choices=STATUS_CHOICES)
    remarks = models.TextField(null=True, blank=True)

    def __str__(self):
        return "ID: %s " % self.pk + self.case_name

    def get_user_role(self):
        return self.role.user.username

    def get_all_tasks(self):
        return self.task_set.all()


class Task(models.Model):
    case = models.ForeignKey(Case, on_delete=models.DO_NOTHING)
    role = models.ForeignKey(UserRole, on_delete=models.DO_NOTHING, default=None)
    task_name = models.CharField(max_length=256, blank=True, null=True)
    task_status = models.PositiveSmallIntegerField(blank=True, null=True, choices=STATUS_CHOICES)
    remarks = models.TextField(null=True, blank=True)

    def __str__(self):
        return "ID: %s " % self.pk + self.task_name

    def get_user_role(self):
        return self.role.user.username

    def get_case_name(self):
        return self.case.case_name
