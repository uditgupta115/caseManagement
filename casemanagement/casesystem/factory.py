import factory
from faker import Factory

from casemanagement.casesystem.models import User, UserRole, Case, Task

fake_data = Factory.create()


class UserFactory(factory.DjangoModelFactory):
    """
        this will create a User instance
    """
    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = factory.LazyAttribute(lambda _: fake_data.user_name())


class UserRoleFactory(factory.DjangoModelFactory):
    """
        this will create a UserRole instance
    """
    class Meta:
        model = UserRole

    role = fake_data.random.randint(1, 2)
    user = factory.SubFactory(UserFactory)


class CaseFactory(factory.DjangoModelFactory):
    """
        this will create a Case instance
    """
    class Meta:
        model = Case

    case_name = factory.LazyAttribute(lambda _: fake_data.name())
    role = factory.SubFactory(UserRoleFactory)
    case_status = fake_data.random.randint(1, 4)
    remarks = fake_data.sentence()


class TaskFactory(factory.DjangoModelFactory):
    """
        this will create a Task instance
    """
    class Meta:
        model = Task

    task_name = factory.LazyAttribute(lambda _: fake_data.name())
    role = factory.SubFactory(UserRoleFactory)
    task_status = fake_data.random.randint(1, 4)
    remarks = fake_data.sentence()
    case = factory.SubFactory(CaseFactory)
