from behave import when, then
import requests
import json

@when(u'the user sends a POST request to {endpoint} with the title "{title}"')
def step_impl(context, endpoint, title):
    context.endpoint = endpoint
    if title == "<empty>":
        title = ""
    context.title = title

    payload = {
        "title": title
    }
    context.payload = payload

    headers = {'Content-Type': 'application/json'}
    response = requests.post(
        f"{context.api_url}{endpoint}",
        json=payload,
        headers=headers
    )

    if response.status_code == 201:
        context.todo_created_responses = []
        context.todo_created_responses.append(response)

    context.response = response

    print(f"POST request sent to {endpoint} with payload: {json.dumps(payload)}")
    print(f"Response status: {response.status_code}")
    print(f"Response body: {response.text}")

@then('the response body contains "{parameter}" of "{value}"')
def step_impl(context, parameter, value):
    if not hasattr(context, 'response'):
        raise AttributeError("No response found in the context. Make sure the POST request was successful.")

    response_json = context.response.json()
    actual_value = response_json.get(parameter)
    if isinstance(actual_value, list):
        actual_value = actual_value[0]
    assert actual_value == value, (
        f"Expected value: '{value}', but got: '{actual_value}'"
    )

    print("Response body validated successfully.")
    print(f"Response: {response_json}")

@then('the system saves the todo item')
def step_impl(context):

    if not hasattr(context, 'response'):
        raise AttributeError("No response found in the context. Make sure the POST request was successful.")

    todo_id = context.response.json().get('id')
    assert todo_id, "The response does not contain an 'id'."

    url = f"{context.api_url}/todos/{todo_id}"
    response = requests.get(url)

    assert response.status_code == 200, f"Failed to retrieve the todo item. Status code: {response.status_code}"

    todos_list = response.json().get('todos', [])
    assert todos_list, "The 'todos' list is empty or missing."

    retrieved_todo = todos_list[0]

    retrieved_todo['doneStatus'] = retrieved_todo['doneStatus'].lower() == 'true'

    retrieved_todo['title'] = retrieved_todo['title']
    expected_title = context.title

    expected_todo = {
        "id": todo_id,
        "title": expected_title,
        "doneStatus": False,
        "description": context.response.json().get('description')
    }

    assert retrieved_todo == expected_todo, (
        f"Expected todo item:\n{expected_todo}\nBut got:\n{retrieved_todo}"
    )

    print("Todo item saved and retrieved successfully.")
    print(f"Retrieved Todo: {retrieved_todo}")

@when(u'the user sends a POST request to {endpoint} with the title name "{title}" and description "{description}"')
def step_impl(context, endpoint, title, description):
    context.endpoint = endpoint
    context.title = title
    context.description = description

    payload = {
        "title": title,
        "description": description
    }
    context.payload = payload

    headers = {'Content-Type': 'application/json'}
    response = requests.post(
        f"{context.api_url}{endpoint}",
        json=payload,
        headers=headers
    )

    if response.status_code == 201:
        context.todo_created_responses = []
        context.todo_created_responses.append(response)

    context.response = response

    print(f"POST request sent to {endpoint} with payload: {json.dumps(payload)}")
    print(f"Response status: {response.status_code}")
    print(f"Response body: {response.text}")


@then('the todo item is not stored in the system')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    url = f"{context.api_url}/todos"
    response = requests.get(url)

    assert response.status_code == 200, f"Failed to retrieve the todo items. Status code: {response.status_code}"

    todos_list = response.json().get('todos', [])

    stored_titles = [todo.get('title') for todo in todos_list]

    assert context.title not in stored_titles, (
        f"The todo item with title '{context.title}' was incorrectly stored in the system."
    )

    print("Verified: The todo item is not stored in the system.")
    print(f"Current Todos: {todos_list}")