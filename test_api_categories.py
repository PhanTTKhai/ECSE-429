import unittest

import requests

BASE_URL = "http://localhost:4567"
JSON_HEADERS = {
    "Accept": "application/json"
}


class TestAPICategories(unittest.TestCase):
    created_cat_ids = []
    created_todo_ids = []

    def tearDown(self):
        """ Delete categories created for the test """
        for id in self.created_cat_ids:
            response = requests.delete(f"{BASE_URL}/categories/{id}")
            self.assertEqual(200, response.status_code)
        self.created_cat_ids.clear()

        for id in self.created_todo_ids:
            response = requests.delete(f"{BASE_URL}/todos/{id}")
            self.assertEqual(200, response.status_code)
        self.created_todo_ids.clear()

    def create_category(self, data):
        response = requests.post(f"{BASE_URL}/categories", json=data)

        if response.status_code == 201:
            try:
                id = int(response.json()['id'])
                self.created_cat_ids.append(id)
                return id
            except (KeyError, ValueError):
                raise Exception("Unexpected response format or missing 'id' field")
        else:
            raise Exception(f"Failed to create category: {response.status_code}")

    def test_get_categories(self):
        """ Test GET /categories """

        response = requests.get(f"{BASE_URL}/categories", headers=JSON_HEADERS)
        self.assertEqual(200, response.status_code)
        self.assertIn("categories", response.json(), "Expected 'categories' field in response")
        self.assertIsInstance(response.json()['categories'], list, "Expected 'categories' field to be a list")


    def test_post_category(self):
        """ Test POST /categories """

        data = {
            "title": "Test Category 1",
            "description": "Test Category Description"
        }
        response = requests.post(f"{BASE_URL}/categories", json=data, headers=JSON_HEADERS)
        
        id = int(response.json()['id'])
        self.created_cat_ids.append(id)

        self.assertEqual(201, response.status_code)
        self.assertEqual(response.json()['title'], data['title'], "Returned title does not match the input title")
        self.assertEqual(response.json()['description'], data['description'],
                         "Returned description does not match the input description")

    def test_put_category(self):
        """ Test PUT /categories """

        data = {
            "title": "Test Category 2",
            "description": "Test Category Description"
        }

        response = requests.put(f"{BASE_URL}/categories", json=data, headers=JSON_HEADERS)
        self.assertEqual(405, response.status_code, "Expected 405 Method Not Allowed")

    def test_get_category_id(self):
        """ Test GET /categories/:id """

        id = self.create_category({
            "title": "Test Category 3",
            "description": "Test Category Description"
        })

        response = requests.get(f"{BASE_URL}/categories/{id}", headers=JSON_HEADERS)
        category_list = response.json()['categories']

        self.assertEqual(200, response.status_code)
        self.assertEqual(len(category_list), 1, "Expected exactly one category to be returned")
        self.assertEqual(int(category_list[0]['id']), id, "Returned id does not match the input id")

    def test_get_category_id_false(self):
        """ Test GET /categories/:id with non-existant category id """

        response = requests.get(f"{BASE_URL}/categories/0", headers=JSON_HEADERS)
        self.assertEqual(404, response.status_code)

    def test_post_category_id(self):
        """ Test POST /categories/:id """

        # Create a category to modify using POST
        id = self.create_category({
            "title": "Test Category 4",
            "description": "Test Category Description"
        })

        data = {
            "title": "Test Category 5",
            "description": "Test Category Description"
        }

        response1 = requests.post(f"{BASE_URL}/categories/{id}", json=data, headers=JSON_HEADERS)
        self.assertEqual(200, response1.status_code)
        self.assertEqual(response1.json()['title'], data['title'], "Returned title does not match the input title")
        self.assertEqual(response1.json()['description'], data['description'], "Returned description does not match the input description")


    def test_post_category_id_empty(self):
        """ Test POST /categories/:id with empty body """

        id = self.create_category({
            "title": "Test Category 6",
            "description": "Test Category Description"
        })

        response = requests.post(f"{BASE_URL}/categories/{id}", headers=JSON_HEADERS)
        self.assertEqual(400, response.status_code, "Expected 400 Bad Request when using POST with empty body")

    def test_put_category_id(self):
        """ Test PUT /categories/:id """

        # Create a category to modify using PUT
        id = self.create_category({
            "title": "Test Category 6",
            "description": "Test Category Description"
        })

        data1 = {
            "title": "Test Category 7",
            "description": "Test Category Description"
        }

        data2 = {}

        response1 = requests.put(f"{BASE_URL}/categories/{id}", json=data1, headers=JSON_HEADERS)
        self.assertEqual(200, response1.status_code)
        self.assertEqual(response1.json()['title'], data1['title'], "Returned title does not match the input title")
        self.assertEqual(response1.json()['description'], data1['description'],
                         "Returned description does not match the input description")

        response2 = requests.put(f"{BASE_URL}/categories/{id}", json=data2, headers=JSON_HEADERS)
        self.assertEqual(400, response2.status_code, "Expected 400 Bad Request when using PUT with empty body")
    
    def test_delete_category_id(self):
        """ Test DELETE /categories/:id """

        id = self.create_category({
            "title": "Test Category 8",
            "description": "Test Category Description"
        })

        response = requests.delete(f"{BASE_URL}/categories/{id}")
        self.assertEqual(200, response.status_code)
        self.created_cat_ids.remove(id)

        response = requests.get(f"{BASE_URL}/categories/{id}", headers=JSON_HEADERS)
        self.assertEqual(404, response.status_code)

    def test_get_categories_id_todos(self):
        """ Test GET /categories/:id/todos """

        cat_id = self.create_category({
            "title": "Test Category 9",
        })

        todo_data = {
            "title": "Todo Test"
        }

        response1 = requests.post(f"{BASE_URL}/todos", json=todo_data, headers=JSON_HEADERS)
        self.assertEqual(201, response1.status_code)
        todo_id = int(response1.json()['id'])
        self.created_todo_ids.append(todo_id)
        
        response2 = requests.post(f"{BASE_URL}/categories/{cat_id}/todos", json={"id": str(todo_id)}, headers=JSON_HEADERS)
        self.assertEqual(201, response2.status_code)

        response3 = requests.get(f"{BASE_URL}/categories/{cat_id}/todos", headers=JSON_HEADERS)
        self.assertEqual(200, response3.status_code)
        self.assertIn("todos", response3.json(), "Expected 'todos' field in response")
        self.assertIsInstance(response3.json()['todos'], list, "Expected 'todos' field to be a list")
        self.assertEqual(len(response3.json()['todos']), 1, "Expected exactly one todo to be returned")
        self.assertEqual(int(response3.json()['todos'][0]['id']), todo_id, "Returned todo id does not match the input todo id")

    def test_get_categories_id_todos_empty(self):
        """ Test GET /categories/:id/todos with non-existant category id """

        cat_id = self.create_category({
            "title": "Test Category 9",
        })

        todo_data = {
            "title": "Todo Test"
        }

        response1 = requests.post(f"{BASE_URL}/todos", json=todo_data, headers=JSON_HEADERS)
        self.assertEqual(201, response1.status_code)
        todo_id = int(response1.json()['id'])
        self.created_todo_ids.append(todo_id)

        # Create the real relationship        
        response2 = requests.post(f"{BASE_URL}/categories/{cat_id}/todos", json={"id": str(todo_id)}, headers=JSON_HEADERS)
        self.assertEqual(201, response2.status_code)

        # Get that todo from a non-existant category (id 0) to show it returns everything instead of nothing
        response3 = requests.get(f"{BASE_URL}/categories/0/todos", headers=JSON_HEADERS)
        self.assertEqual(200, response3.status_code)
        self.assertIn("todos", response3.json(), "Expected 'todos' field in response")
        self.assertIsInstance(response3.json()['todos'], list, "Expected 'todos' field to be a list")
        self.assertEqual(len(response3.json()['todos']), 0, "Expected zero todo items to be returned")

    def test_put_categories_id_todos(self):
        """ Test PUT /categories/:id/todos """

        id = self.create_category({
            "title": "Test Category 10",
        })
        response = requests.put(f"{BASE_URL}/categories/{id}/todos", headers=JSON_HEADERS)
        self.assertEqual(405, response.status_code, "Expected 405 Method Not Allowed")

    def test_delete_categories_id_todos(self):
        """ Test DELETE /categories/:id/todos """

        id = self.create_category({
            "title": "Test Category 11",
        })

        response = requests.delete(f"{BASE_URL}/categories/{id}/todos")
        self.assertEqual(405, response.status_code)

    def test_get_categories_id_todos_id(self):
        """ Test GET /categories/:id/todos/:id """

        cat_id = self.create_category({
            "title": "Test Category 12",
        })

        todo_data = {
            "title": "Todo Test"
        }

        response1 = requests.post(f"{BASE_URL}/todos", json=todo_data, headers=JSON_HEADERS)
        self.assertEqual(201, response1.status_code)
        todo_id = int(response1.json()['id'])
        self.created_todo_ids.append(todo_id)
        
        response2 = requests.post(f"{BASE_URL}/categories/{cat_id}/todos", json={"id": str(todo_id)}, headers=JSON_HEADERS)
        self.assertEqual(201, response2.status_code)

        response3 = requests.get(f"{BASE_URL}/categories/{cat_id}/todos/{todo_id}", headers=JSON_HEADERS)
        self.assertEqual(404, response3.status_code)

# Running the tests
if __name__ == '__main__':
    unittest.main()
