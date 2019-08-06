import factory

from casemanagement.casesystem.models import User, UserRole, Case, Task


class UserFactory(factory.DjangoModelFactory):
    """
        this will create a User instance
    """
    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = 'john'


class UserRoleFactory(factory.DjangoModelFactory):
    """
        this will create a UserRole instance
    """
    class Meta:
        model = UserRole

    role = 1
    user = factory.SubFactory(UserFactory)


class CaseFactory(factory.DjangoModelFactory):
    """
        this will create a Case instance
    """
    class Meta:
        model = Case

    case_name = "case_"
    role = UserRoleFactory()


class TaskFactory(factory.DjangoModelFactory):
    """
        this will create a Task instance
    """
    class Meta:
        model = Task

    task_name = "task_"
