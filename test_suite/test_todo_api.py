import unittest
import requests
import xml.etree.ElementTree as ET


class TestAPITodos(unittest.TestCase):
    BASE_URL = "http://localhost:4567"
    json_headers = {
        "Accept": "application/json"
    }
    xml_headers = {
        "Accept": "application/xml",
        "Content-Type": "application/xml"
    }
    created_todo_ids = []

    def tearDown(self):
        """ Delete todos created for the test """
        for todo_id in self.created_todo_ids:
            response = requests.delete(f"{self.BASE_URL}/todos/{todo_id}")
            self.assertEqual(200, response.status_code)
        self.created_todo_ids.clear()

    def create_todo(self, data):
        response = requests.post(f"{self.BASE_URL}/todos", json=data)

        if response.status_code == 201:
            try:
                todo_id = response.json()['id']
                self.created_todo_ids.append(todo_id)
                return int(todo_id)
            except (KeyError, ValueError):
                raise Exception("Unexpected response format or missing 'id' field")
        else:
            raise Exception(f"Failed to create todo: {response.status_code}")

    def test_get_todos_json(self):
        for i in range(1, 4):
            todo_data = {
                "title": f"Test Todo {i}",
            }
            self.create_todo(todo_data)

        response = requests.get(f"{self.BASE_URL}/todos", headers=self.json_headers)
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.headers['Content-Type'], "application/json")

        # Generate the expected titles
        num_todos = 3
        todos = response.json()['todos']
        created_titles = [f"Test Todo {i}" for i in range(1, num_todos + 1)]
        titles = [todo['title'] for todo in todos]

        for created_title in created_titles:
            self.assertIn(created_title, titles, f"Todo with title '{created_title}' was not found")

    def test_post_todo_json(self):
        todo_data = {
            "title": "Test Todo",
        }
        response = requests.post(f"{self.BASE_URL}/todos", json=todo_data, headers=self.json_headers)
        todo_id = response.json()['id']
        self.created_todo_ids.append(todo_id)
        self.assertEqual(201, response.status_code)
        self.assertEqual(response.headers['Content-Type'], "application/json")

    def test_head_todos_json(self):
        response = requests.head(f"{self.BASE_URL}/todos", headers=self.json_headers)
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.headers['Content-Type'], "application/json")

    def test_put_todo_not_allowed_json(self):
        todo_data = {
            "title": "Test Todo",
        }
        response = requests.put(f"{self.BASE_URL}/todos", json=todo_data, headers=self.json_headers)
        self.assertEqual(405, response.status_code,
                         "Expected 405 Method Not Allowed when sending PUT to /todos without an ID")

    def test_delete_todo_not_allowed_json(self):
        todo_data = {
            "title": "Test Todo",
        }
        todo_id = self.create_todo(todo_data)

        delete_data = {
            "id": str(todo_id),
        }

        response = requests.delete(f"{self.BASE_URL}/todos", json=delete_data, headers=self.json_headers)
        self.assertEqual(405, response.status_code, "Expected 405 Method Not Allowed when sending a DELETE with a body")

    def test_get_todos_xml(self):
        for i in range(1, 4):
            todo_data = {
                "title": f"Test Todo {i}",
            }
            self.create_todo(todo_data)

        response = requests.get(f"{self.BASE_URL}/todos", headers=self.xml_headers)
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.headers['Content-Type'], "application/xml")

        # Generate the expected titles
        num_todos = 3
        root = ET.fromstring(response.text)
        created_titles = [f"Test Todo {i}" for i in range(1, num_todos + 1)]
        titles = [todo.find('title').text for todo in root.findall('todo')]

        for created_title in created_titles:
            self.assertIn(created_title, titles, f"Todo with title '{created_title}' was not found")

    def test_post_todo_xml(self):
        todo_data = """
                <todo>
                    <title>Test Todo</title>
                </todo>
                """
        response = requests.post(f"{self.BASE_URL}/todos", data=todo_data, headers=self.xml_headers)
        root = ET.fromstring(response.text)
        todo_id = root.find('id').text
        self.created_todo_ids.append(todo_id)
        self.assertEqual(201, response.status_code)
        self.assertEqual(response.headers['Content-Type'], "application/xml")

    def test_head_todos_xml(self):
        response = requests.head(f"{self.BASE_URL}/todos", headers=self.xml_headers)
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.headers['Content-Type'], "application/xml")

    def test_put_todo_not_allowed_xml(self):
        todo_data = """
                        <todo>
                            <title>Test Todo</title>
                        </todo>
                        """
        response = requests.put(f"{self.BASE_URL}/todos", data=todo_data, headers=self.xml_headers)
        self.assertEqual(405, response.status_code,
                         "Expected 405 Method Not Allowed when sending PUT to /todos without an ID")

    def test_delete_todo_not_allowed_xml(self):
        todo_data = {
            "title": "Test Todo",
        }
        todo_id = self.create_todo(todo_data)

        todo_data = f"""
                        <todo>
                            <id>{str(todo_id)}</id>
                        </todo>
                        """
        response = requests.delete(f"{self.BASE_URL}/todos", data=todo_data, headers=self.xml_headers)
        self.assertEqual(405, response.status_code, "Expected 405 Method Not Allowed when sending a DELETE with a body")


# Running the tests
if __name__ == '__main__':
    unittest.main()
