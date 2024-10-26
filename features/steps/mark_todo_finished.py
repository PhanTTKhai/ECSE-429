from behave import given, when, then
import requests
import json
import difflib


@when('the user update the todo task "{title}" as "{status}"')
def step_impl(context, title, status):
    todo_id = context.todo_created_responses[0].json().get('id')
    headers = {'Content-Type': 'application/json'}
    if status == "finished":
        payload = {
            'doneStatus': True  # Mark as finished
        }
    if status == "not finished":
        payload = {
            'doneStatus': False  # Mark as finished
        }
    # Send a PUT request to update the todo
    response = requests.put(f"{context.api_url}/todos/{todo_id}", json=payload, headers=headers)

    # Store the response for validation
    context.response = response

    assert response.status_code == 200, (
        f"Failed to update todo: {title}. Status: {response.status_code}"
    )
    print(f"Updated todo: {title} as finished.")

@when('the user update the todo task with id "{todo_id}" as "{status}"')
def step_impl(context, todo_id, status):
    headers = {'Content-Type': 'application/json'}
    if status == "finished":
        payload = {
            'doneStatus': True  # Mark as finished
        }
    if status == "not finished":
        payload = {
            'doneStatus': False  # Mark as finished
        }
    # Send a PUT request to update the todo
    response = requests.put(f"{context.api_url}/todos/{todo_id}", json=payload, headers=headers)

    # Store the response for validation
    context.response = response

@then('the system updates the todo item "doneStatus" to "{status}"')
def step_impl(context, status):
    """
    Verify that the system updated the todo item's doneStatus to finished.
    """
    updated_todo = context.response.json()
    if status == "finished":
        assert updated_todo['doneStatus'] == "true", (
            f"Expected doneStatus: true, but got: {updated_todo['doneStatus']}."
        )
    if status == "not finished":
        assert updated_todo['doneStatus'] == "false", (
            f"Expected doneStatus: true, but got: {updated_todo['doneStatus']}."
        )
    print("Validated: Todo item's doneStatus is " + status)

@given('there is no todo item with id "{id}"')
def step_impl(context, id):
    """
    Ensure there is no todo item with the specified ID and store the initial state of todos.
    """
    # Check if the specific todo item exists using a GET request
    url = f"{context.api_url}/todos/{id}"
    response = requests.get(url)

    # If the response is 404, the item doesn't exist, which is expected
    if response.status_code == 404:
        print(f"Validated: No todo item found with id '{id}'.")
    else:
        # If the item exists, raise an error
        assert response.status_code == 404, (
            f"Expected no todo item with id '{id}', but found one with status {response.status_code}."
        )

    # Retrieve the full list of todos to store the initial state
    response = requests.get(f"{context.api_url}/todos")
    assert response.status_code == 200, "Failed to retrieve the full list of todos."

    # Store the initial state of todos
    context.initial_todos = response.json().get('todos', [])
    print("Stored the initial state of todos.")

@then('the system does not create or modify any todo items')
def step_impl(context):
    """
    Verify that no new todo items were created or modified.
    """
    # Send a GET request to retrieve the current state of todos
    response = requests.get(f"{context.api_url}/todos")
    assert response.status_code == 200, "Failed to retrieve todos."

    # Store the current state of todos
    current_todos = response.json().get('todos', [])

    # Ensure the state of todos has not changed
    initial_todos_json = json.dumps(context.initial_todos, indent=2)
    current_todos_json = json.dumps(current_todos, indent=2)

    # If the lists are different, print only the differences
    if initial_todos_json != current_todos_json:
        diff = difflib.unified_diff(
            initial_todos_json.splitlines(),
            current_todos_json.splitlines(),
            fromfile='Initial Todos',
            tofile='Current Todos',
            lineterm=''
        )
        print("\n".join(diff))  # Print only the differences
    assert current_todos == context.initial_todos, (
        "The system created or modified todo items unexpectedly."
    )

    print("Validated: No new todo items were created or modified.")