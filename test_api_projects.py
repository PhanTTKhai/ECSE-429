import unittest
import requests


class TestAPIProjects(unittest.TestCase):
    BASE_URL = "http://localhost:4567"
    json_headers = {
        "Accept": "application/json"
    }
    created_project_ids = []
    created_todo_ids = []
    created_category_ids = []

    def test_service_is_running(self):
        try:
            response = requests.get('http://localhost:4567/')
            self.assertEqual(response.status_code, 200)
        except requests.exceptions.ConnectionError:
            self.fail("Service is not running!")

    def tearDown(self):
        """ Delete created projects, todos, and categories """
        for project_id in self.created_project_ids:
            response = requests.delete(f"{self.BASE_URL}/projects/{project_id}", headers=self.json_headers)
            if response.status_code != 404:
                self.assertEqual(200, response.status_code)
        for todo_id in self.created_todo_ids:
            response = requests.delete(f"{self.BASE_URL}/todos/{todo_id}", headers=self.json_headers)
            if response.status_code != 404:
                self.assertEqual(200, response.status_code)
        for category_id in self.created_category_ids:
            response = requests.delete(f"{self.BASE_URL}/categories/{category_id}", headers=self.json_headers)
            if response.status_code != 404:
                self.assertEqual(200, response.status_code)
        self.created_project_ids.clear()
        self.created_todo_ids.clear()
        self.created_category_ids.clear()

    def create_project(self, project_data):
        """Utility function to create a project and return its ID."""
        response = requests.post(f"{self.BASE_URL}/projects", json=project_data, headers=self.json_headers)
        if response.status_code != 201:
            print("Failed to create project:", response.json())  # Print error for debugging
        self.assertEqual(201, response.status_code)
        return response.json()["id"]

    def create_todo(self, data):
        response = requests.post(f"{self.BASE_URL}/todos", json=data, headers=self.json_headers)
        self.assertEqual(201, response.status_code)
        if 'id' in response.json():
            todo_id = response.json()['id']
            self.created_todo_ids.append(todo_id)
            return todo_id
        raise Exception("Failed to retrieve todo ID from response")

    def create_category(self, data):
        response = requests.post(f"{self.BASE_URL}/categories", json=data, headers=self.json_headers)
        self.assertEqual(201, response.status_code)
        if 'id' in response.json():
            category_id = response.json()['id']
            self.created_category_ids.append(category_id)
            return category_id
        raise Exception("Failed to retrieve category ID from response")

    # Tests for /projects and /projects/:id
    def test_get_projects(self):
        response = requests.get(f"{self.BASE_URL}/projects", headers=self.json_headers)
        self.assertEqual(200, response.status_code)
        self.assertIn('projects', response.json(), "Expected 'projects' field in response")

    def test_post_project(self):
        project_data = {"title": "Test Project"}
        response = requests.post(f"{self.BASE_URL}/projects", json=project_data, headers=self.json_headers)
        self.assertEqual(201, response.status_code)
        project_id = response.json()['id']
        self.created_project_ids.append(project_id)

    def test_get_specific_project(self):
        """Test retrieving a specific project by ID."""
        data = {"title": "Project for Retrieval", "description": "Testing specific project retrieval"}
        creation_response = requests.post(f"{self.BASE_URL}/projects", json=data)
        project_id = creation_response.json()["id"]
        response = requests.get(f"{self.BASE_URL}/projects/{project_id}")
        self.assertEqual(response.status_code, 200)
        project_data = response.json().get("projects", [{}])[0]
        self.assertEqual(project_data["id"], str(project_id))
        self.assertEqual(project_data["title"], data["title"])
        self.assertEqual(project_data["description"], data["description"])

    def test_put_project_expected_behavior(self):
        """Test expected behavior: only specified fields should be updated, others remain unchanged."""
        project_data = {
            "title": "Initial Project",
            "description": "Original description",
            "completed": False,
            "active": True
        }
        project_id = self.create_project(project_data)
        updated_data = {"title": "Updated Project"}
        put_response = requests.put(f"{self.BASE_URL}/projects/{project_id}", json=updated_data,
                                    headers=self.json_headers)
        self.assertEqual(200, put_response.status_code, "Expected status code 200 for successful update.")
        updated_project_response = requests.get(f"{self.BASE_URL}/projects/{project_id}", headers=self.json_headers)
        updated_project = updated_project_response.json()["projects"][0]
        self.assertEqual(updated_project["title"], "Updated Project")
        self.assertEqual(updated_project["description"], "Original description",
                         "Expected 'description' to remain unchanged.")
        self.assertEqual(updated_project["completed"], "false", "Expected 'completed' to remain unchanged.")
        self.assertEqual(updated_project["active"], "true", "Expected 'active' to remain unchanged.")

    def test_put_project_actual_behavior(self):
        """Observed behavior: Unspecified fields are reset or removed upon update."""
        project_data = {
            "title": "Initial Project",
            "description": "Original description",
            "completed": False,
            "active": True
        }
        project_id = self.create_project(project_data)
        updated_data = {"title": "Updated Project"}
        put_response = requests.put(f"{self.BASE_URL}/projects/{project_id}", json=updated_data,
                                    headers=self.json_headers)
        self.assertEqual(200, put_response.status_code)
        updated_project_response = requests.get(f"{self.BASE_URL}/projects/{project_id}", headers=self.json_headers)
        updated_project = updated_project_response.json()["projects"][0]
        self.assertEqual(updated_project["title"], "Updated Project")
        self.assertEqual(updated_project["completed"], "false", "Unexpected behavior: 'completed' field was modified.")
        self.assertEqual(updated_project["active"], "false", "Unexpected behavior: 'active' field was modified.")

    def test_delete_project(self):
        project_id = self.create_project({"title": "Temporary Project"})
        response = requests.delete(f"{self.BASE_URL}/projects/{project_id}", headers=self.json_headers)
        self.assertEqual(200, response.status_code)

    def test_options_projects(self):
        response = requests.options(f"{self.BASE_URL}/projects", headers=self.json_headers)
        self.assertEqual(200, response.status_code)

    def test_method_not_allowed_for_projects(self):
        response = requests.put(f"{self.BASE_URL}/projects", json={"title": "Unauthorized Project"},
                                headers=self.json_headers)
        self.assertEqual(405, response.status_code)

    # Tests for /projects/:id/tasks and /projects/:id/categories
    def test_get_project_tasks_expected_behavior(self):
        """Test actual behavior: retrieving tasks for an invalid project ID."""
        non_existent_project_id = "999999999"

        response = requests.get(f"{self.BASE_URL}/projects/{non_existent_project_id}", headers=self.json_headers)
        self.assertEqual(404, response.status_code, "Expected status code 404 for non-existent project ID.")

        response = requests.get(f"{self.BASE_URL}/projects/{non_existent_project_id}/tasks", headers=self.json_headers)
        self.assertEqual(200, response.status_code, "Expected status code 404 for non-existent project ID.")

    def test_get_project_tasks_actual_behavior(self):
        """Test actual behavior: retrieving tasks for a non-existent project ID."""
        non_existent_project_id = "999999999"
        response = requests.get(f"{self.BASE_URL}/projects/{non_existent_project_id}", headers=self.json_headers)
        self.assertEqual(404, response.status_code, "Expected status code 404 for non-existent project ID.")

        response = requests.get(f"{self.BASE_URL}/projects/{non_existent_project_id}/tasks", headers=self.json_headers)
        self.assertEqual(200, response.status_code, "Expected status code 404 for non-existent project ID.")

    def test_post_project_task_relationship(self):
        project_id = self.create_project({"title": "Project for Task Relation"})
        todo_id = self.create_todo({"title": "Task for Project"})
        response = requests.post(f"{self.BASE_URL}/projects/{project_id}/tasks", json={"id": todo_id},
                                 headers=self.json_headers)
        self.assertEqual(201, response.status_code)

    def test_delete_project_task_relationship(self):
        project_id = self.create_project({"title": "Project for Task Deletion"})
        todo_id = self.create_todo({"title": "Task to Remove"})
        requests.post(f"{self.BASE_URL}/projects/{project_id}/tasks", json={"id": todo_id}, headers=self.json_headers)
        response = requests.delete(f"{self.BASE_URL}/projects/{project_id}/tasks/{todo_id}", headers=self.json_headers)
        self.assertEqual(200, response.status_code)

    def test_options_project_tasks(self):
        project_id = self.create_project({"title": "Project for OPTIONS"})
        response = requests.options(f"{self.BASE_URL}/projects/{project_id}/tasks", headers=self.json_headers)
        self.assertEqual(200, response.status_code)

    def test_get_project_categories(self):
        project_id = self.create_project({"title": "Project for Category Test"})
        response = requests.get(f"{self.BASE_URL}/projects/{project_id}/categories", headers=self.json_headers)
        self.assertEqual(200, response.status_code)
        self.assertIn("categories", response.json(), "Expected 'categories' field in response")

    def test_post_project_category_relationship(self):
        project_id = self.create_project({"title": "Project for Category Relation"})
        category_id = self.create_category({"title": "Category for Project"})
        response = requests.post(f"{self.BASE_URL}/projects/{project_id}/categories", json={"id": category_id},
                                 headers=self.json_headers)
        self.assertEqual(201, response.status_code)

    def test_delete_project_category_relationship(self):
        project_id = self.create_project({"title": "Project for Category Deletion"})
        category_id = self.create_category({"title": "Category to Remove"})
        requests.post(f"{self.BASE_URL}/projects/{project_id}/categories", json={"id": category_id},
                      headers=self.json_headers)
        response = requests.delete(f"{self.BASE_URL}/projects/{project_id}/categories/{category_id}",
                                   headers=self.json_headers)
        self.assertEqual(200, response.status_code)

    def test_options_project_categories(self):
        project_id = self.create_project({"title": "Project for OPTIONS"})
        response = requests.options(f"{self.BASE_URL}/projects/{project_id}/categories", headers=self.json_headers)
        self.assertEqual(200, response.status_code)

    # Tests for /projects/:id/tasks/:id and /projects/:id/categories/:id
    def test_delete_specific_task_relationship(self):
        project_id = self.create_project({"title": "Project for Task Relationship Deletion"})
        todo_id = self.create_todo({"title": "Related Task"})
        requests.post(f"{self.BASE_URL}/projects/{project_id}/tasks", json={"id": todo_id}, headers=self.json_headers)
        response = requests.delete(f"{self.BASE_URL}/projects/{project_id}/tasks/{todo_id}", headers=self.json_headers)
        self.assertEqual(200, response.status_code)

    def test_options_specific_task_relationship(self):
        project_id = self.create_project({"title": "Project for Task OPTIONS"})
        todo_id = self.create_todo({"title": "Task for OPTIONS"})
        response = requests.options(f"{self.BASE_URL}/projects/{project_id}/tasks/{todo_id}", headers=self.json_headers)
        self.assertEqual(200, response.status_code)

    def test_delete_specific_category_relationship_expected_behavior(self):
        """Test expected behavior: deleting a specific category relationship."""
        project_id = self.create_project({"title": "Project for Category Relationship Deletion"})
        category_id = self.create_category({"title": "Related Category"})

        # Create the relationship
        requests.post(f"{self.BASE_URL}/projects/{project_id}/categories", json={"id": category_id},
                      headers=self.json_headers)

        # Delete the relationship
        response = requests.delete(f"{self.BASE_URL}/projects/{project_id}/categories/{category_id}",
                                   headers=self.json_headers)
        self.assertEqual(200, response.status_code, "Expected status code 200 for successful deletion.")

        # Verify that the relationship has been deleted
        check_response = requests.get(f"{self.BASE_URL}/projects/{project_id}/categories", headers=self.json_headers)
        self.assertEqual(200, check_response.status_code, "Expected status code 200 for checking categories.")

        categories = check_response.json().get("categories", [])
        self.assertNotIn(category_id, [cat["id"] for cat in categories],
                         "Expected category ID to be removed from project.")

    def test_delete_specific_category_relationship_actual_behavior(self):
        """Test actual behavior: verify that the relationship was not deleted."""
        project_id = self.create_project({"title": "Project for Category Relationship Deletion"})
        category_id = self.create_category({"title": "Related Category"})

        # Create the relationship
        requests.post(f"{self.BASE_URL}/projects/{project_id}/categories", json={"id": category_id},
                      headers=self.json_headers)

        # Delete the relationship
        response = requests.delete(f"{self.BASE_URL}/projects/{project_id}/categories/{category_id}",
                                   headers=self.json_headers)
        self.assertEqual(200, response.status_code, "Expected status code 200 for deletion attempt.")

        # Verify that the relationship still exists, indicating a bug
        check_response = requests.get(f"{self.BASE_URL}/projects/{project_id}/categories", headers=self.json_headers)
        self.assertEqual(200, check_response.status_code, "Expected status code 200 for checking categories.")

        categories = check_response.json().get("categories", [])
        self.assertIn(category_id, [cat["id"] for cat in categories],
                      "Expected category ID to still be present in project, indicating deletion failed.")


# Running the tests
if __name__ == '__main__':
    unittest.main()
