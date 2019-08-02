from django.db.models import QuerySet
from django.test import TestCase, Client

# Create your tests here.
from casemanagement.casesystem.models import User, Case, UserRole, Task


def initial_setup():
    u1 = User.objects.create(username='root', is_active=True)
    set_password(u1, 'root')
    u2 = User.objects.create(username='daffo')
    set_password(u2, 'root')
    UserRole.objects.create(user_id=1, role=1)
    UserRole.objects.create(user_id=2, role=2)
    Case.objects.create(role_id=1, case_name="test_case")
    Task.objects.create(role_id=2, case_id=1, task_name="test_task")


def set_password(user, password):
    user.set_password(password)
    user.save()


class UserCase(TestCase):
    def setUp(self) -> None:
        initial_setup()

    def test_get_user_role(self):
        case1 = Case.objects.get(case_name="test_case")
        self.assertEqual(case1.get_user_role(), 'root')

    def test_all_task(self):
        case1 = Case.objects.get(case_name="test_case")
        self.assertEqual(type(case1.get_all_tasks()), QuerySet)

    def test_checking_task(self):
        case1 = Task.objects.get(task_name="test_task")
        self.assertEqual(case1.get_case_name(), 'test_case')


class LoginViewCase(TestCase):
    def test_manager_login_function(self):
        initial_setup()
        c = Client()
        login = c.post('/login/', {'username': 'root', 'password': 'root'})
        self.assertURLEqual(login.url, '/manager/')

    def test_task_manager_login_function(self):
        initial_setup()
        c = Client()
        login = c.post('/login/', {'username': 'daffo', 'password': 'root'})
        self.assertURLEqual(login.url, '/task-manager/')

