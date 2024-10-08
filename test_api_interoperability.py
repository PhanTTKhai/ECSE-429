import unittest

import requests


class TestAPIInteroperability(unittest.TestCase):
    BASE_URL = "http://localhost:4567"
    json_headers = {
        "Accept": "application/json"
    }
    created_todo_ids = []
    created_categories_ids = []
    created_projects_ids = []

    ### helper functions ###

    def tearDown(self):
        for todo_id in self.created_todo_ids:
            response = requests.delete(f"{self.BASE_URL}/todos/{todo_id}", headers=self.json_headers)
            self.assertEqual(response.status_code, 200, f"Failed to delete todo {todo_id}")
        self.created_todo_ids.clear()

        for category_id in self.created_categories_ids:
            response = requests.delete(f"{self.BASE_URL}/categories/{category_id}", headers=self.json_headers)
            self.assertEqual(response.status_code, 200, f"Failed to delete category {category_id}")
        self.created_categories_ids.clear()

        for project_id in self.created_projects_ids:
            response = requests.delete(f"{self.BASE_URL}/projects/{project_id}", headers=self.json_headers)
            self.assertEqual(response.status_code, 200, f"Failed to delete project {project_id}")
        self.created_projects_ids.clear()

    def create_todo(self, todo_data):
        response = requests.post(f"{self.BASE_URL}/todos", json=todo_data, headers=self.json_headers)
        if response.status_code == 201:
            todo_id = response.json().get('id')
            if todo_id:
                self.created_todo_ids.append(todo_id)
                return todo_id
            else:
                raise Exception("Unexpected response format or missing 'id' field")
        else:
            raise Exception(f"Failed to create todo: {response.status_code} - {response.text}")

    def create_category(self, category_data):
        response = requests.post(f"{self.BASE_URL}/categories", json=category_data, headers=self.json_headers)
        if response.status_code == 201:
            category_id = response.json().get('id')
            if category_id:
                self.created_categories_ids.append(category_id)
                return category_id
            else:
                raise Exception("Unexpected response format or missing 'id' field")
        else:
            raise Exception(f"Failed to create todo: {response.status_code} - {response.text}")

    def create_project(self, project_data):
        response = requests.post(f"{self.BASE_URL}/projects", json=project_data, headers=self.json_headers)
        if response.status_code == 201:
            project_id = response.json().get('id')
            if project_id:
                self.created_projects_ids.append(project_id)
                return project_id
            else:
                raise Exception("Unexpected response format or missing 'id' field")
        else:
            raise Exception(f"Failed to create todo: {response.status_code} - {response.text}")

    ### tests ###

    def test_delete_category_from_todo(self):
        todo_id = self.create_todo({"title": "Test Todo for delete"})
        category_id = self.create_category({"title": "Test Category for delete"})

        # note creating relationship based on title, since id doesn't work
        link_response = requests.post(f"{self.BASE_URL}/todos/{todo_id}/categories", json={"id": category_id},
                                      headers=self.json_headers)
        self.assertEqual(link_response.status_code, 201,
                         f"Failed to link category to todo: {link_response.status_code} {link_response.text}")

        # TESTED FUNCTIONALITY
        delete_response = requests.delete(f"{self.BASE_URL}/todos/{todo_id}/categories/{category_id}",
                                          headers=self.json_headers)
        self.assertEqual(delete_response.status_code, 200,
                         f"Failed to delete category {category_id} from todo {todo_id}: {delete_response.status_code} {delete_response.text}")

        # verifying no relationship exists anymore
        get_response = requests.get(f"{self.BASE_URL}/todos/{todo_id}/categories", headers=self.json_headers)
        self.assertEqual(get_response.status_code, 200,
                         f"Failed to get categories for todo {todo_id}: {get_response.status_code}")

        categories = get_response.json().get('categories', [])
        category_ids = [cat['id'] for cat in categories]

        self.assertNotIn(category_id, category_ids, "Category is still linked to the todo after deletion")


if __name__ == '__main__':
    unittest.main()
