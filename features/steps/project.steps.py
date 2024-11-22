import difflib
import json

import requests
from behave import when, then, given


# Update Project Feature
@given('a project with title "{title}" exists')
def step_impl(context, title):
    payload = {"title": title}
    headers = {'Content-Type': 'application/json'}
    
    response = requests.post(f"{context.api_url}/projects", json=payload, headers=headers)
    
    assert response.status_code == 201, f"Failed to create project with ID {id}. Status: {response.status_code}"
    
    if not hasattr(context, 'project_created_responses'):
        context.project_created_responses = []
    context.project_created_responses.append(response)
    
    context.project_id = response.json().get("id", id)
    context.project_title = title

@when('the user sends a POST request to the corresponding /projects/id with a new title "{new_title}"')
def step_impl(context, new_title):
    assert hasattr(context, 'project_id'), "Project ID not found in context."
    
    payload = {"title": new_title}
    headers = {'Content-Type': 'application/json'}
    
    project_url = f"{context.api_url}/projects/{context.project_id}"
    context.response = requests.post(project_url, json=payload, headers=headers)
    
    context.updated_title = new_title

@when('the user sends a PUT request to the corresponding /projects/id with a new title "{new_title}"')
def step_impl(context, new_title):
    assert hasattr(context, 'project_id'), "Project ID not found in context."
    
    payload = {"title": new_title}
    headers = {'Content-Type': 'application/json'}
    
    project_url = f"{context.api_url}/projects/{context.project_id}"
    context.response = requests.put(project_url, json=payload, headers=headers)
    
    context.updated_title = new_title


@then('the project response body confirms "title" as "{expected_title}"')
def step_impl(context, expected_title):
    response_json = context.response.json()
    actual_title = response_json.get("title")
    assert actual_title == expected_title, (
        f"Expected title '{expected_title}', but got '{actual_title}'."
    )

@when('the user sends a PUT request to /projects/{id} with a new title "{new_title}"')
def step_impl(context, id, new_title):
    payload = {"title": new_title}
    headers = {'Content-Type': 'application/json'}
    
    context.response = requests.put(f"{context.api_url}/projects/{id}", json=payload, headers=headers)
    
    context.updated_title = new_title
    context.project_id = id

@then('the system updates the project')
def step_impl(context):
    response = requests.get(f"{context.api_url}/projects/{context.project_id}")
    
    assert response.status_code == 200, f"Failed to retrieve the project. Status: {response.status_code}"
    
    project_data = response.json().get("projects", [{}])[0]
    
    assert project_data.get("title") == context.updated_title, (
        f"Expected updated title '{context.updated_title}', but got '{project_data.get('title')}'."
    )

@then('the project is not stored in the system')
def step_impl(context):
    response = requests.get(f"{context.api_url}/projects/{context.project_id}")
    
    assert response.status_code == 404, (
        f"Expected project with ID {context.project_id} to not exist, but it was found with status code {response.status_code}."
    )


# Create Project Feature

import requests
from behave import when

@when('the user sends a POST request to /projects with title "{title}" and description "{description}"')
def step_impl(context, title, description):
    payload = {
        "title": title,
        "description": description
    }
    headers = {'Content-Type': 'application/json'}
    
    context.response = requests.post(f"{context.api_url}/projects", json=payload, headers=headers)
    
    context.project_title = title
    context.project_description = description
    
    if context.response.status_code == 201:
        if not hasattr(context, 'project_created_responses'):
            context.project_created_responses = []
        context.project_created_responses.append(context.response)

@when('the user sends a POST request to /projects with empty title and description')
def step_impl(context):
    payload = {
        "title": "",
        "description": ""
    }
    
    headers = {'Content-Type': 'application/json'}
    
    context.response = requests.post(f"{context.api_url}/projects", json=payload, headers=headers)
    
    context.project_title = payload["title"]
    context.project_description = payload["description"]
    
    if context.response.status_code == 201:
        if not hasattr(context, 'project_created_responses'):
            context.project_created_responses = []
        context.project_created_responses.append(context.response)


@then('the response body confirms "title" of "{expected_title}" and "description" of "{expected_description}"')
def step_impl(context, expected_title, expected_description):
    response_json = context.response.json()
    
    actual_title = response_json.get("title")
    actual_description = response_json.get("description")
    
    assert actual_title == expected_title, (
        f"Expected title '{expected_title}', but got '{actual_title}'."
    )
    assert actual_description == expected_description, (
        f"Expected description '{expected_description}', but got '{actual_description}'."
    )

@then('the system saves the project')
def step_impl(context):
    project_id = context.response.json().get("id")
    assert project_id, "The response does not contain an 'id'."

    context.project_id = project_id

    response = requests.get(f"{context.api_url}/projects/{project_id}")
    
    assert response.status_code == 200, f"Failed to retrieve the project. Status: {response.status_code}"
    
    project_data = response.json().get("projects", [{}])[0]
    
    assert project_data.get("title") == context.project_title, (
        f"Expected title '{context.project_title}', but got '{project_data.get('title')}'."
    )
    if hasattr(context, 'project_description'):
        assert project_data.get("description") == context.project_description, (
            f"Expected description '{context.project_description}', but got '{project_data.get('description')}'."
        )


@when('the user sends a POST request to /projects with an ID "{id}"')
def step_impl(context, id):
    payload = {
        "id": id,
        "title": f"Project {id}"  
    }
    headers = {'Content-Type': 'application/json'}
    
    context.response = requests.post(f"{context.api_url}/projects", json=payload, headers=headers)
    
    context.project_id = id
    context.project_title = payload["title"]

# Delete Step Features

@given('a project with ID "{id}" exists')
def step_impl(context, id):
    response = requests.get(f"{context.api_url}/projects/{id}")
    
    if response.status_code == 200:
        project_data = response.json().get("projects", [{}])[0]
        print(f"Project with ID {id} already exists. Using existing project.")
    else:
        payload = {"id": id, "title": f"Project {id}"}
        headers = {'Content-Type': 'application/json'}
        
        response = requests.post(f"{context.api_url}/projects", json=payload, headers=headers)
        
        assert response.status_code == 201, f"Failed to create project with ID {id}. Status: {response.status_code}"
        
        project_data = response.json()
        print(f"Project with ID {id} created successfully.")
    
    if not hasattr(context, 'project_created_responses'):
        context.project_created_responses = []
    context.project_created_responses.append(response)
    
    context.project_id = project_data.get("id", id)
    context.project_title = project_data.get("title", f"Project {id}")

@given('the initial project list is captured')
def step_impl(context):
    response = requests.get(f"{context.api_url}/projects")
    assert response.status_code == 200, f"Failed to retrieve initial projects list. Status: {response.status_code}"
    context.initial_projects = response.json().get("projects", [])

@given('tasks are associated with the project')
def step_impl(context):
    # Ensure the project ID is available in the context
    assert hasattr(context, 'project_id'), "Project ID not found in context. Ensure the project was created in a previous step."
    
    # Check if there are tasks associated with the project
    response = requests.get(f"{context.api_url}/projects/{context.project_id}/tasks")
    assert response.status_code == 200, f"Failed to retrieve tasks for project {context.project_id}. Status: {response.status_code}"
    
    tasks = response.json().get("tasks", [])

    if not tasks:
        # No tasks are associated, so create a new task
        payload = {
            "title": "Associated Task",
            "description": "Task automatically created and associated with the project"
        }
        headers = {'Content-Type': 'application/json'}
        
        # Create the task
        task_response = requests.post(f"{context.api_url}/todos", json=payload, headers=headers)
        assert task_response.status_code == 201, f"Failed to create a task. Status: {task_response.status_code}"
        
        # Extract the created task ID
        task_id = task_response.json().get("id")
        
        # Associate the task with the project by including task_id in the body
        assoc_payload = {"task_id": task_id}
        assoc_response = requests.post(f"{context.api_url}/projects/{context.project_id}/tasks", json=assoc_payload, headers=headers)
        assert assoc_response.status_code == 200, f"Failed to associate task {task_id} with project {context.project_id}. Status: {assoc_response.status_code}"
        
        print(f"Task with ID {task_id} created and associated with project {context.project_id}.")
    else:
        print(f"Project {context.project_id} already has tasks associated.")


@when('the user sends a DELETE request using the corresponding projects id')
def step_impl(context):
    assert hasattr(context, 'project_id'), "Project ID not found in context."
    
    project_url = f"{context.api_url}/projects/{context.project_id}"
    context.response = requests.delete(project_url)
    
    assert context.response.status_code in [200, 204], (
        f"Failed to delete project with ID {context.project_id}. Status: {context.response.status_code}"
    )

@then('the system removes the project from the database')
def step_impl(context):
    assert hasattr(context, 'project_id'), "Project ID not found in context."
    
    response = requests.get(f"{context.api_url}/projects/{context.project_id}")
    
    assert response.status_code == 404, (
        f"Expected project with ID {context.project_id} to be deleted, but it was found with status code {response.status_code}."
    )

@given('there is no project with id "{project_id}"')
def step_impl(context, project_id):
    response = requests.get(f"{context.api_url}/projects/{project_id}")
    
    # Assert that the project does not exist (should return 404)
    assert response.status_code == 404, (
        f"Expected no project with ID {project_id}, but found one with status code {response.status_code}."
    )

@when('the user sends a DELETE request with id "{project_id}"')
def step_impl(context, project_id):
    context.response = requests.delete(f"{context.api_url}/projects/{project_id}")
    
    context.project_id = project_id


@then('the system does not create or modify any projects')
def step_impl(context):
    response = requests.get(f"{context.api_url}/projects")
    assert response.status_code == 200, f"Failed to retrieve projects list. Status: {response.status_code}"
    
    current_projects = response.json().get("projects", [])
    
    assert current_projects == context.initial_projects, (
        "The system created or modified projects unexpectedly. "
        f"Expected projects: {context.initial_projects}, but got: {current_projects}"
    )

@then("the system removes the project and its associated tasks from the database")
def step_impl(context):
    # Ensure the project ID is available in the context
    assert hasattr(context, 'project_id'), "Project ID not found in context. Ensure the project was created and stored in a previous step."
    
    # Verify that the project has been deleted
    project_response = requests.get(f"{context.api_url}/projects/{context.project_id}")
    assert project_response.status_code == 404, (
        f"Expected project with ID {context.project_id} to be deleted, but it was found with status code {project_response.status_code}."
    )
    
    # Verify that each associated task has been deleted
    assert hasattr(context, 'task_ids'), "Task IDs not found in context. Ensure tasks were associated with the project."
    for task_id in context.task_ids:
        task_response = requests.get(f"{context.api_url}/tasks/{task_id}")
        assert task_response.status_code == 404, (
            f"Expected task with ID {task_id} to be deleted, but it was found with status code {task_response.status_code}."
        )
    
    print(f"Project {context.project_id} and all associated tasks have been successfully removed from the database.")


# Get Steps Features

@when('the user sends a GET request to with the corresponding projects id')
def step_impl(context):
    assert hasattr(context, 'project_id'), "Project ID not found in context."
    
    context.response = requests.get(f"{context.api_url}/projects/{context.project_id}")
    
    assert context.response.status_code == 200, (
        f"Expected status code 200, but got {context.response.status_code}."
    )

@then('the response body confirms the correct id and corresponding title')
def step_impl(context):
    response_json = context.response.json()
    
    project_data = response_json.get("projects", [{}])[0]
    
    assert str(project_data.get("id")) == str(context.project_id), (
        f"Expected project ID {context.project_id}, but got {project_data.get('id')}."
    )
    
    assert project_data.get("title") == context.project_title, (
        f"Expected project title '{context.project_title}', but got '{project_data.get('title')}'."
    )

@when('the user sends a GET request with id "{id}"')
def step_impl(context, id):
    context.response = requests.get(f"{context.api_url}/projects/{id}")
    
    context.project_id = id

@when("the user sends a GET request to retrieve the project through the tasks' project association")
def step_impl(context):
    # Ensure that project ID and at least one associated task are set in context
    assert hasattr(context, "project_id"), "Project ID is not set in context."
    assert hasattr(context, "task_id"), "Task ID is not set in context."

    # Send GET request to retrieve the project through the task's project association
    task_url = f"{context.api_url}/tasks/{context.task_id}/project"
    context.response = requests.get(task_url)

    # Confirm that the request was successful
    assert context.response.status_code == 200, (
        f"Expected status code 200, but got {context.response.status_code}."
    )

# View All Projects Step Features

@given('at least one project exists')
def step_impl(context):
    response = requests.get(f"{context.api_url}/projects")
    assert response.status_code == 200, "Failed to retrieve projects list."

    projects = response.json().get("projects", [])
    if not projects:
        payload = {"title": "Default Project"}
        headers = {'Content-Type': 'application/json'}
        
        create_response = requests.post(f"{context.api_url}/projects", json=payload, headers=headers)
        assert create_response.status_code == 201, "Failed to create a default project to ensure at least one exists."

@given('at least {min_projects:d} project exists')
def step_impl(context, min_projects):
    response = requests.get(f"{context.api_url}/projects")
    assert response.status_code == 200, f"Failed to retrieve projects list. Status: {response.status_code}"
    
    projects = response.json().get("projects", [])
    existing_count = len(projects)

    projects_to_create = max(0, min_projects - existing_count)

    for i in range(projects_to_create):
        payload = {"title": f"Auto Project {existing_count + i + 1}"}
        headers = {'Content-Type': 'application/json'}
        create_response = requests.post(f"{context.api_url}/projects", json=payload, headers=headers)
        
        assert create_response.status_code == 201, (
            f"Failed to create project. Status: {create_response.status_code}"
        )
        
        if not hasattr(context, 'project_created_responses'):
            context.project_created_responses = []
        context.project_created_responses.append(create_response)

    context.project_count = min_projects


@when('the user sends a GET request on /projects')
def step_impl(context):
    context.response = requests.get(f"{context.api_url}/projects")
    
    assert context.response.status_code == 200, (
        f"Expected status code 200, but got {context.response.status_code}."
    )

@when('the user sends a GET request to retrieve each project by its ID')
def step_retrieve_each_project_by_id(context):
    assert hasattr(context, 'initial_projects'), "The initial project list was not captured."

    context.project_responses = []

    for project in context.initial_projects:
        project_id = project.get("id")
        assert project_id is not None, "Project ID not found in initial project list."

        response = requests.get(f"{context.api_url}/projects/{project_id}")
        
        context.project_responses.append(response)

        print(f"Retrieved project with ID {project_id} with status {response.status_code}.")

@then('each response body confirms the correct project ID and title')
def step_verify_correct_project_id_and_title(context):
    assert hasattr(context, 'initial_projects'), "Initial project list not found in context."
    assert hasattr(context, 'project_responses'), "Project responses not found in context."
    assert len(context.initial_projects) == len(context.project_responses), (
        "Mismatch between number of initial projects and number of responses."
    )

    for project, response in zip(context.initial_projects, context.project_responses):
        project_id = project.get("id")
        project_title = project.get("title")
        
        assert response.status_code == 200, (
            f"Expected status code 200 for project with ID {project_id}, but got {response.status_code}."
        )
        
        response_data = response.json().get("projects", [{}])[0]
        actual_id = response_data.get("id")
        actual_title = response_data.get("title")
        
        assert str(actual_id) == str(project_id), (
            f"Expected project ID {project_id}, but got {actual_id}."
        )
        assert actual_title == project_title, (
            f"Expected project title '{project_title}', but got '{actual_title}'."
        )

@then('the API responds with status code 200 (OK) for each project')
def step_verify_status_code_200_for_each_project(context):
    assert hasattr(context, 'initial_projects'), "The initial project list was not captured."

    for project in context.initial_projects:
        project_id = project.get("id")
        assert project_id is not None, "Project ID not found in initial project list."

        response = requests.get(f"{context.api_url}/projects/{project_id}")
        
        assert response.status_code == 200, (
            f"Expected status code 200 for project ID {project_id}, but got {response.status_code}."
        )

        print(f"Project with ID {project_id} retrieved successfully with status 200.")

@then('the response body contains all projects')
def step_impl(context):
    response_json = context.response.json()
    
    current_projects = response_json.get("projects", [])
    
    assert current_projects == context.initial_projects, (
        f"Expected projects list to match initial capture. "
        f"Initial projects: {context.initial_projects}, but got: {current_projects}"
    )

@given('no projects exist')
def step_impl(context):
    response = requests.get(f"{context.api_url}/projects")
    assert response.status_code == 200, f"Failed to retrieve projects list. Status: {response.status_code}"

    projects = response.json().get("projects", [])

    for project in projects:
        project_id = project.get("id")
        delete_response = requests.delete(f"{context.api_url}/projects/{project_id}")
        assert delete_response.status_code in [200, 204], (
            f"Failed to delete project with ID {project_id}. Status: {delete_response.status_code}"
        )

    response = requests.get(f"{context.api_url}/projects")
    assert response.status_code == 200, f"Failed to retrieve projects list after deletion. Status: {response.status_code}"
    projects_after_deletion = response.json().get("projects", [])
    assert len(projects_after_deletion) == 0, "Expected no projects to exist, but some are still present."

@when('the user submits a GET request to /projects/')
def step_impl(context):
    context.response = requests.get(f"{context.api_url}/projects/")