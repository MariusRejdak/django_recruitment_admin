from datetime import date
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
import json

from staff.models import Employee, Department, Project


class RestTestCase(TestCase):
    """A few sample functional tests"""

    def setUp(self):
        self.client = APIClient()
        self.admin_client = APIClient()

        self.adminuser = User.objects.create_superuser(
            username="admin", email="admin@test.com", password="admin1234"
        )
        self.admin_client.login(username="admin", password="admin1234")

        self.management = Department.objects.create(name="management")
        self.developers = Department.objects.create(name="developers")
        self.ceo = Employee.objects.create(
            first_name="Mighty",
            last_name="CEO",
            hired_date=date(2017, 1, 1),
            department=self.management,
        )
        self.developer = Employee.objects.create(
            first_name="Just",
            last_name="Dev",
            hired_date=date(2018, 2, 1),
            department=self.developers,
            manager=self.ceo,
        )

        self.recruitment = Project.objects.create(
            name="recruitment",
            description="Recruiting new employees",
            deadline=None,
            department=self.management,
            hidden=True,
        )
        self.website = Project.objects.create(
            name="website",
            description="New company website",
            deadline=date(2018, 12, 31),
            department=self.developers,
            hidden=False,
        )

    def test_hidden_project_admin(self):
        response = self.client.get(f"/admin/projects/{self.recruitment.id}/")
        self.assertEqual(403, response.status_code)  # Unauthorized

        response = self.admin_client.get(f"/admin/projects/{self.recruitment.id}/")
        self.assertEqual(200, response.status_code)
        data = json.loads(response.content)
        self.assertEqual(self.recruitment.id, data["id"])
        self.assertIn("description", data)

    def test_project_public(self):
        reponse = self.client.get(f"/public/projects/{self.recruitment.id}/")
        self.assertEqual(404, reponse.status_code)

        response = self.client.get(f"/public/projects/{self.website.id}/")
        self.assertEqual(200, response.status_code)
        data = json.loads(response.content)
        self.assertNotIn("description", data)

        response = self.client.get(f"/public/projects/{self.website.id}/")
        self.assertEqual(200, response.status_code)
        data = json.loads(response.content)
        self.assertNotIn("description", data)

        response = self.client.post(
            "/public/projects/",
            {
                "id": 2,
                "name": "website",
                "deadline": date(2018, 12, 31),
                "department": self.developers.id,
            },
        )
        self.assertEqual(405, response.status_code)  # Method Not Allowed

    def test_empleyees_public(self):
        response = self.client.get("/public/employees/")
        self.assertEqual(403, response.status_code)  # Unauthorized

        response = self.admin_client.get("/public/employees/")
        self.assertEqual(200, response.status_code)

        response = self.admin_client.get(f"/public/employees/{self.developer.id}/")
        self.assertEqual(200, response.status_code)
        data = json.loads(response.content)
        self.assertNotIn("manager", data)

    def test_empleyees_admin(self):
        response = self.admin_client.get(f"/admin/employees/{self.developer.id}/")
        self.assertEqual(200, response.status_code)
        data = json.loads(response.content)
        self.assertEqual(data["manager"], self.ceo.id)
