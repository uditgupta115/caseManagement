from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.db.models import QuerySet
from django.test import TestCase, Client
from selenium.webdriver.android.webdriver import WebDriver

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
        c = Client(enforce_csrf_checks=False)
        login = c.post('/login/', {'username': 'daffo', 'password': 'root'})
        # self.assertEqual(login.status_code, 200)
        self.assertURLEqual(login.get, '/task-manager/')

    def test_get_login_page(self):
        initial_setup()
        c = Client()
        login = c.get('/login/')
        self.assertEqual(login.status_code, 200)

    def test_create_case_system_via_api(self):
        initial_setup()
        c = Client()
        login = c.post(
            '/api/case/',
            {
                "role": 1,
                "task": [
                    {
                        "role": 2,
                        "task_name": "task_via_api_test"
                    }
                ],
                "case_name": "case_via_api_test",
             },
            headers={'Content-Type': 'application/json'}
        )
        # create status code
        self.assertEqual(login.status_code, 201)

    def test_update_case_system_via_api(self):
        initial_setup()
        c = Client()
        response = c.patch(
            '/api/case/1/',
            {
                "role": 1,
                "task": [
                    {
                        "role": 2,
                        "task_name": "task_via_api_test"
                    }
                ],
                "case_name": "case_via_api_test_update",
             },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

    def test_get_case_system_via_api(self):
        initial_setup()
        c = Client()
        response = c.get(
            '/api/case/1/',
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_case_system_via_api(self):
        initial_setup()
        c = Client()
        response = c.delete(
            '/api/case/1/',
        )
        # empty response status as destroy mixins return the same
        self.assertEqual(response.status_code, 204)


class TestHelloView(TestCase):
    def test_hello(self):
        c = Client()
        sd = c.get('/hello/')
        self.assertEquals(str(sd.content), 'b\'Hello, World!\'')


class MySeleniumTests(StaticLiveServerTestCase):
    # fixtures = ['user-data.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        self.selenium.get('%s%s' % ('http://127.0.0.1:8000', '/login/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('root')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('root')
        self.selenium.find_element_by_name('submit').click()
