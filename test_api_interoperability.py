import unittest
import requests
import subprocess
import time

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
        
        #note creating relationship based on title, since id doesn't work
        link_response = requests.post(f"{self.BASE_URL}/todos/{todo_id}/categories", json={"id": category_id}, headers=self.json_headers)
        self.assertEqual(link_response.status_code, 201, f"Failed to link category to todo: {link_response.status_code} {link_response.text}")

        # TESTED FUNCTIONALITY
        delete_response = requests.delete(f"{self.BASE_URL}/todos/{todo_id}/categories/{category_id}", headers=self.json_headers)
        self.assertEqual(delete_response.status_code, 200, f"Failed to delete category {category_id} from todo {todo_id}: {delete_response.status_code} {delete_response.text}")
        
        # verifying no relationship exists anymore
        get_response = requests.get(f"{self.BASE_URL}/todos/{todo_id}/categories", headers=self.json_headers)
        self.assertEqual(get_response.status_code, 200, f"Failed to get categories for todo {todo_id}: {get_response.status_code}")
        
        categories = get_response.json().get('categories', [])
        category_ids = [cat['id'] for cat in categories]
        
        self.assertNotIn(category_id, category_ids, "Category is still linked to the todo after deletion")
    
    
    ### POST TODOS/ID/CATEGORIES ###

    def test_post_todo_category_should_succeed_but_fails(self):
        todo_id = self.create_todo({"title": "Test Todo with ID"})
        category_id = self.create_category({"title": "Test Category with ID"})

        link_response = requests.post(f"{self.BASE_URL}/todos/{todo_id}/categories", json={"id": category_id}, headers=self.json_headers)

        self.assertEqual(link_response.status_code, 201, f"Expected success (201 Created), but got failure.")

    def test_post_todo_category_succeeds_with_title(self):
        todo_id = self.create_todo({"title": "Test Todo with Title"})
        category_title = "Test Category with Title"
        category_id = self.create_category({"title": category_title})

        # create relationship using 'title'
        link_response = requests.post(f"{self.BASE_URL}/todos/{todo_id}/categories", json={"title": category_title}, headers=self.json_headers)
        self.assertEqual(link_response.status_code, 201, f"Expected success when linking with title, but got: {link_response.status_code}")

    def test_post_todo_category_no_todo(self):
        category_title = "Test Category with Title"
        category_id = self.create_category({"title": category_title})

        # expected failure: linking category to non-existent todo
        non_existent_todo_id = 999999  # assuming this ID does not exist
        link_invalid_todo_response = requests.post(f"{self.BASE_URL}/todos/{non_existent_todo_id}/categories", json={"title": category_title}, headers=self.json_headers)
        self.assertEqual(link_invalid_todo_response.status_code, 404, "Expected 404 when linking to non-existent todo")
        
    def test_post_todo_category_no_category(self):
        todo_id = self.create_todo({"title": "Test Todo with Title"})
        # expected failure: linking non-existent category to an existing todo
        non_existent_category_title = "Non-existent Category" #this category has not been created
        link_invalid_category_response = requests.post(f"{self.BASE_URL}/todos/{todo_id}/categories", json={"title": non_existent_category_title}, headers=self.json_headers)
        self.assertEqual(link_invalid_category_response.status_code, 404, "Expected 404 when linking non-existent category to a valid todo")

    def test_post_todo_category_no_todo_no_category(self):
        non_existent_todo_id = 999999  # assuming this ID does not exist
        non_existent_category_title = "Non-existent Category" #this category has not been created
        # expected failure: both todo and category don't exist
        link_invalid_both_response = requests.post(f"{self.BASE_URL}/todos/{non_existent_todo_id}/categories", json={"title": non_existent_category_title}, headers=self.json_headers)
        self.assertEqual(link_invalid_both_response.status_code, 404, "Expected 404 when both todo and category are non-existent")
        

    ### POST /TODOS/ID/CATEGORIES/ID ###

    def test_post_todo_category_by_id(self):
        todo_id = self.create_todo({"title": "Test Todo with ID Linking"})
        category_id = self.create_category({"title": "Test Category with ID Linking"})

        link_response = requests.post(f"{self.BASE_URL}/todos/{todo_id}/categories/{category_id}", headers=self.json_headers)

        self.assertNotEqual(link_response.status_code, 201, "Linking using /todos/:id/categories/:id should not work.")
        self.assertIn(link_response.status_code, [404], f"Expected failure but got: {link_response.status_code}")

    ### GET /TODOS/ID/CATEGORIES/ID ###

    def test_get_todo_category_by_id(self):
        todo_id = self.create_todo({"title": "Test Todo with ID Linking"})
        category_id = self.create_category({"title": "Test Category with ID Linking"})

        get_response = requests.get(f"{self.BASE_URL}/todos/{todo_id}/categories/{category_id}", headers=self.json_headers)

        self.assertEqual(get_response.status_code, 404, f"Expected 404 Not Found but got: {get_response.status_code}")

    ### POST /TODOS/ID/TASK-OF ###

    def test_post_todo_list_task_of(self):
        todo_id = self.create_todo({"title": "Test Todo for Task Of"})
        project_id = self.create_project({"title": "Test Project for Task Of"})

        link_response = requests.post(f"{self.BASE_URL}/todos/{todo_id}/task-of", json={"id": project_id}, headers=self.json_headers)
        self.assertEqual(link_response.status_code, 201, f"Failed to link todo to project: {link_response.status_code}")

    
    ### GET /TODOS/ID/TASK-OF ###

    def test_get_todo_list_task_of(self):
        todo_id = self.create_todo({"title": "Test Todo for Task Of"})
        project_id = self.create_project({"title": "Test Project for Task Of"})

        link_response = requests.post(f"{self.BASE_URL}/todos/{todo_id}/task-of", json={"id": project_id}, headers=self.json_headers)
        self.assertEqual(link_response.status_code, 201, f"Failed to link todo to project: {link_response.status_code}")

        get_response = requests.get(f"{self.BASE_URL}/todos/list/task-of", headers=self.json_headers)
        self.assertEqual(get_response.status_code, 200, f"Failed to get task-of list: {get_response.status_code}")

        task_of_list = get_response.json().get('todos', [])
        task_of_ids = [task['id'] for task in task_of_list]

        self.assertIn(todo_id, task_of_ids, "Todo is not listed under task-of")
      
    def test_get_todo_list_task_of_non_existing_task(self):
        non_existent_todo_id = 999999
        get_response = requests.get(f"{self.BASE_URL}/todos/{non_existent_todo_id}/task-of", headers=self.json_headers)
        self.assertEqual(get_response.status_code, 404, f"Expected 404 Not Found, but got: {get_response.status_code}")
        print(f"Response for GET /todos/{non_existent_todo_id}/task-of: {get_response.status_code}")


    ### /TODOS/ID/TASK-OF/ID ###

    def test_delete_todo_task_of(self):
        todo_id = self.create_todo({"title": "Test Todo for Task Of"})
        project_id = self.create_project({"title": "Test Project for Task Of"})
        
        link_response = requests.post(f"{self.BASE_URL}/todos/{todo_id}/task-of", json={"id": project_id}, headers=self.json_headers)
        self.assertEqual(link_response.status_code, 201, f"Failed to link todo to project: {link_response.status_code} - {link_response.text}")
        
        delete_response = requests.delete(f"{self.BASE_URL}/todos/{todo_id}/task-of/{project_id}", headers=self.json_headers)
        self.assertEqual(delete_response.status_code, 200, f"Failed to delete task-of link: {delete_response.status_code} - {delete_response.text}")
        
        get_response = requests.get(f"{self.BASE_URL}/todos/{todo_id}/task-of", headers=self.json_headers)
        task_of_list = get_response.json().get('projects', [])
        project_ids = [project['id'] for project in task_of_list]
        
        self.assertNotIn(project_id, project_ids, "Project is still linked to the todo after deletion")


    ### GET /CATEGORIES/ID/PROJECTS ###

    def test_get_category_projects(self):
        category_id = self.create_category({"title": "Test Category with Projects"})
        project_id = self.create_project({"title": "Test Project for Category"})

        link_response = requests.post(f"{self.BASE_URL}/categories/{category_id}/projects", json={"id": project_id}, headers=self.json_headers)
        self.assertEqual(link_response.status_code, 201, f"Failed to link category to project: {link_response.status_code} - {link_response.text}")

        get_response = requests.get(f"{self.BASE_URL}/categories/{category_id}/projects", headers=self.json_headers)
        self.assertEqual(get_response.status_code, 200, f"Failed to get projects for category: {get_response.status_code} - {get_response.text}")

        projects_list = get_response.json().get('projects', [])
        project_ids = [project['id'] for project in projects_list]

        self.assertIn(project_id, project_ids, "Project is not linked to the category")


    ### POST /CATEGORIES/ID/PROJECTS ###

    def test_post_category_project(self):
        category_id = self.create_category({"title": "Test Category for Project"})
        project_id = self.create_project({"title": "Test Project for Category"})

        link_response = requests.post(f"{self.BASE_URL}/categories/{category_id}/projects", json={"id": project_id}, headers=self.json_headers)
        self.assertEqual(link_response.status_code, 201, f"Failed to link category to project: {link_response.status_code} - {link_response.text}")

    def test_post_category_todo_using_title(self): #using title
        category_id = self.create_category({"title": "Test Category for Todo"})
        todo_id = self.create_todo({"title": "Test Todo for Category"})

        link_response = requests.post(f"{self.BASE_URL}/categories/{category_id}/todos", json={"title": "Test Todo for Category"}, headers=self.json_headers)
        self.assertEqual(link_response.status_code, 201, f"Failed to link category to todo using title: {link_response.status_code} - {link_response.text}")

    ### DELETE /CATEGORIES/ID/PROJECTS/ID ###

    def test_delete_category_todo(self):
        category_id = self.create_category({"title": "Test Category for Todo Deletion"})
        todo_id = self.create_todo({"title": "Test Todo for Deletion"})

        link_response = requests.post(f"{self.BASE_URL}/categories/{category_id}/todos", json={"id": todo_id}, headers=self.json_headers)
        self.assertEqual(link_response.status_code, 201, f"Failed to link category to todo: {link_response.status_code} - {link_response.text}")

        delete_response = requests.delete(f"{self.BASE_URL}/categories/{category_id}/todos/{todo_id}", headers=self.json_headers)
        self.assertEqual(delete_response.status_code, 200, f"Failed to delete todo from category: {delete_response.status_code} - {delete_response.text}")

    def test_delete_non_existing_category_todo(self):
        category_id = self.create_category({"title": "Test Category for Non-Existing Todo Deletion"})
        non_existent_todo_id = 999999

        delete_response = requests.delete(f"{self.BASE_URL}/categories/{category_id}/todos/{non_existent_todo_id}", headers=self.json_headers)
        self.assertEqual(delete_response.status_code, 404, f"Expected 404 Not Found when trying to delete a non-existing relationship, but got: {delete_response.status_code} - {delete_response.text}")

    
    #### POST CATEGORIES/ID/TODOS/ID ###

    def test_post_category_id_todo_id(self):
        category_id = self.create_category({"title": "Test Category for Undocumented Todo"})
        todo_id = self.create_todo({"title": "Test Todo for Category"})

        link_response = requests.post(f"{self.BASE_URL}/categories/{category_id}/todos/{todo_id}", headers=self.json_headers)
        self.assertEqual(link_response.status_code, 404, f"Expected 404 Not Found for undocumented POST, but got: {link_response.status_code} - {link_response.text}")

    #### GET CATEGORIES/ID/TODOS/ID ###

    def test_get_category_id_todo_id(self):
        category_id = self.create_category({"title": "Test Category for Undocumented Todo"})
        todo_id = self.create_todo({"title": "Test Todo for Category"})

        get_response = requests.get(f"{self.BASE_URL}/categories/{category_id}/todos/{todo_id}", headers=self.json_headers)
        self.assertEqual(get_response.status_code, 404, f"Expected 404 Not Found for undocumented GET, but got: {get_response.status_code} - {get_response.text}")


if __name__ == '__main__':
    unittest.main()
