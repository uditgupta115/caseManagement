from django.db.models import QuerySet
from django.test import TestCase, Client
from faker import Factory

from casemanagement.casesystem.factory import UserFactory, UserRoleFactory, \
    CaseFactory, TaskFactory
from casemanagement.casesystem.models import Case, Task

# from selenium.webdriver.firefox.webdriver import WebDriver
# from django.contrib.staticfiles.testing import StaticLiveServerTestCase

fake = Factory.create()


class CustomTestCase(TestCase):

    def setUp(self) -> None:
        # self.case1_user = User.objects.create(username='case1',
        #                                       is_active=True)
        # self.case2_user = User.objects.create(username='case2',
        #                                       is_active=True)
        # self.task1_user = User.objects.create(username='task1')
        # self.task2_user = User.objects.create(username='task2')
        # self.set_password(self.case1_user, 'root')
        # self.set_password(self.case2_user, 'root')
        # self.set_password(self.task1_user, 'root')
        # self.set_password(self.task2_user, 'root')
        # self.ur_case_1 = UserRole.objects.create(
        #     user=self.case1_user, role=1)
        # self.ur_case_2 = UserRole.objects.create(
        #     user=self.case2_user, role=1)
        # self.ur_task_1 = UserRole.objects.create(
        #     user=self.task1_user, role=2)
        # self.ur_task_2 = UserRole.objects.create(
        #     user=self.task2_user, role=2)
        # self.case1 = Case.objects.create(role=self.ur_case_1,
        #                                  case_name="test_case1")
        # self.case2 = Case.objects.create(role=self.ur_case_2,
        #                                  case_name="test_case2")
        self.task1 = Task.objects.create(
            role=self.ur_task_1, case=self.case1, task_name="test_task1")
        self.task2 = Task.objects.create(
            role=self.ur_task_1, case=self.case1, task_name="test_task2")
        self.task3 = Task.objects.create(
            role=self.ur_task_2, case=self.case2, task_name="test_task3")
        self.task4 = Task.objects.create(
            role=self.ur_task_2, case=self.case2, task_name="test_task4")

        for i in range(1, 5):
            setattr(self, 'user%s' % i, UserFactory(username=fake.name()))
            self.set_password(getattr(self, 'user%s' % i), 'root')

        for i in range(1, 5):
            setattr(self, 'userrole%s' % i, UserRoleFactory(
                user=getattr(self, 'user%s' % i), role=1 if i < 3 else 2))

        for i in range(1, 3):
            setattr(self, 'case%s' % i, CaseFactory(
                case_name=fake.name(),
                role=getattr(self, 'userrole%s' % i)
            ))
        for i in range(1, 5):
            setattr(self, 'task%s' % i, TaskFactory(
                task_name=fake.name(),
                role=getattr(self, 'userrole%s' % fake.random.randint(3, 4)),
                # role=getattr(self, 'userrole%s' % 3 if i < 3 else 4),
                case=getattr(self, 'case%s' % fake.random.randint(1, 2))
                ))

    @staticmethod
    def set_password(user, password):
        user.set_password(password)
        user.save()

# class TestCasesSetup:
#
#     def __init__(self):
#         self.user1 = UserFactory(username='test_case', is_active=True)
#         self.user2 = UserFactory(username='test_task')
#         # set_password(self.user1, 'root')
#         # set_password(self.user2, 'root')
#         self.userrole1 = UserRoleFactory(user=self.user1, role=1)
#         self.userrole2 = UserRoleFactory(user=self.user2, role=2)
#         self.case1 = CaseFactory(role=self.userrole1, case_name="test_case")
#         self.case2 = TaskFactory(role=self.userrole2, case_id=1,
#         task_name="test_task")


class UserCase(CustomTestCase):
    """
        testing case/tasks and roles of users.
    """

    def test_get_case_username(self):
        case1 = Case.objects.get(id=self.case1.pk)
        self.assertEqual(case1.get_user_role(), self.case1.role.user.username)
        self.assertNotEqual(case1.get_user_role(),
                            self.case2.role.user.username)

    def test_get_task_username(self):
        task1 = Task.objects.get(id=self.task1.pk)
        self.assertEqual(task1.get_user_role(), self.task1.role.user.username)
        self.assertNotEqual(task1.get_user_role(),
                            self.task2.role.user.username)

    def test_cases_all_tasks(self):
        case1 = Case.objects.get(id=self.case1.pk)
        self.assertEqual(type(case1.get_all_tasks()), QuerySet)
        self.assertEqual(case1.get_all_tasks().count(),
                         Task.objects.filter(case=self.case1).count())

    def test_test_case_name(self):
        task1 = Task.objects.get(id=self.task1.pk)
        self.assertEqual(task1.get_case_name(), task1.case.case_name)
        # self.assertNotEqual(task1.get_case_name(), task1.case.case_name)


class LoginViewTestCase(CustomTestCase):
    """
    checking whether login redirecting functionality is
    landing on correct page or not.
    """

    def test_manager_login_with_correct_credentials(self):
        c = Client()
        login = c.post('/login/', {'username': self.user1, 'password': 'root'})
        self.assertEqual(login.status_code, 302)
        self.assertURLEqual(login.url, '/manager/')

    def test_task_manager_login_with_correct_credentials(self):
        c = Client(enforce_csrf_checks=False)
        login = c.post('/login/', {'username': self.user4, 'password': 'root'})
        self.assertEqual(login.status_code, 302)
        self.assertURLEqual(login.url, '/task-manager/')

    def test_manager_login_with_incorrect_credentials(self):
        c = Client()
        login = c.post('/login/', {'username': self.user3, 'password': 'root'})
        self.assertEqual(login.status_code, 302)
        self.assertNotEqual(login.url, '/manager/')

    def test_task_manager_login_with_incorrect_credentials(self):
        c = Client()
        login = c.post('/login/', {'username': self.user2, 'password': 'root'})
        self.assertEqual(login.status_code, 302)
        self.assertNotEqual(login.url, '/task-manager/')

    def test_get_login_page(self):
        c = Client()
        login = c.get('/login/')
        self.assertEqual(login.status_code, 200)


class CaseSystemApiCases(CustomTestCase):
    """
        Testing CRUD Operations via Apis.
    """

    def test_create_case_system_via_api(self):
        c = Client()
        response = c.post(
            '/api/case/',
            data={
                "role": 1,
                "task": [{
                    "task_name": "task_via_api_test",
                    "role": 2,
                }],
                "case_name": "case_via_api_test",
            },
            headers={'Content-Type': 'application/json'}
        )
        # checking whether object is being created or not
        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(Case.objects.get(case_name='case_via_api_test'),
                              Case)
        # self.assertIsInstance(Task.objects.get(
        # task_name='task_via_api_test'), Task)

    def test_update_case_system_via_api(self):
        c = Client()
        self.assertEqual(Case.objects.get(id=self.case1.pk).case_name,
                         self.case1.case_name)
        response = c.patch(
            '/api/case/%s/' % self.case1.pk,
            {
                # "role": 1,
                # "task": [
                #     {
                #         "role": 2,
                #         "task_name": "task_via_api_test"
                #     }
                # ],
                "case_name": "case_via_api_test_update",
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Case.objects.get(id=self.case1.pk).case_name,
                         'case_via_api_test_update')

    def test_get_case_system_via_api(self):
        c = Client()
        response = c.get(
            '/api/case/%s/' % self.case1.pk,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['case_name'],
                         Case.objects.get(id=self.case1.pk).case_name)

    def test_delete_case_system_via_api(self):
        c = Client()
        self.assertIsNotNone(Case.objects.filter(id=self.case1.pk))
        response = c.delete(
            '/api/case/%s/' % self.case1.pk,
        )
        # empty response status as destroy mixins return the same
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Case.objects.filter(id=self.case1.pk).count(), 0)


class TestHelloView(TestCase):
    def test_hello(self):
        c = Client()
        sd = c.get('/hello/')
        self.assertEquals(str(sd.content), 'b\'Hello, World!\'')

# class MySeleniumTests(StaticLiveServerTestCase):
#
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         cls.selenium = WebDriver()
#         cls.selenium.implicitly_wait(10)
#
#     @classmethod
#     def tearDownClass(cls):
#         cls.selenium.quit()
#         super().tearDownClass()
#
#     def test_login(self):
#         self.selenium.get('%s%s' % ('http://127.0.0.1:8000', '/login/'))
#         username_input = self.selenium.find_element_by_name("username")
#         username_input.send_keys('root')
#         password_input = self.selenium.find_element_by_name("password")
#         password_input.send_keys('root')
#         self.selenium.find_element_by_name('submit').click()
