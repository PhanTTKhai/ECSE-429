import difflib
import json

import requests
from behave import when, then, given


@given('there are todo items stored in the system')
def step_impl(context):
    headers = {'Content-Type': 'application/json'}
    context.todo_created_responses = []
    context.todo_title_id_map = {}
    for row in context.table:
        payload = {
            'title': row['title'],
            'doneStatus': row['doneStatus'].lower() == 'true',
            'description': row['description']
        }

        response = requests.post(f"{context.api_url}/todos", json=payload, headers=headers)

        assert response.status_code == 201, (
            f"Failed to create todo: {row['title']}. Status: {response.status_code}"
        )
        context.todo_created_responses.append(response)
        todo_id = response.json().get('id')
        context.todo_title_id_map[row['title']] = todo_id


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


@then('the todo item is not stored in the system')
def step_impl(context):
    url = f"{context.api_url}/todos"
    response = requests.get(url)

    assert response.status_code == 200, f"Failed to retrieve the todo items. Status code: {response.status_code}"

    todos_list = response.json().get('todos', [])

    stored_titles = [todo.get('title') for todo in todos_list]

    assert context.title not in stored_titles, (
        f"The todo item with title '{context.title}' was incorrectly stored in the system."
    )


@when('the user update the "{parameter}" of todo task "{title}" to "{new_value}" with {method}')
def step_impl(context, parameter, title, new_value, method):
    todo_id = context.todo_title_id_map.get(title)

    headers = {'Content-Type': 'application/json'}

    if parameter == "doneStatus":
        payload = {
            'doneStatus': new_value == "finished"
        }
    else:
        payload = {parameter: new_value}

    if method == "PUT":
        response = requests.put(
            f"{context.api_url}/todos/{todo_id}",
            json=payload,
            headers=headers
        )
        context.response = response
    elif method == "POST":
        response = requests.post(
            f"{context.api_url}/todos/{todo_id}",
            json=payload,
            headers=headers
        )
        context.response = response
    else:
        print("Only accept POST and PUT methods.")

    context.response = response

    assert response.status_code == 200, (
        f"Failed to update todo: {title}. Status: {response.status_code} Error: {response.json().get('errorMessages')}"
    )


@when('the user update the todo task with id "{todo_id}" as "{status}"')
def step_impl(context, todo_id, status):
    headers = {'Content-Type': 'application/json'}
    if status == "finished":
        payload = {
            'doneStatus': True
        }
    if status == "not finished":
        payload = {
            'doneStatus': False
        }
    response = requests.put(f"{context.api_url}/todos/{todo_id}", json=payload, headers=headers)

    context.response = response


@then('the system updates the todo item "{field}" to "{value}"')
def step_impl(context, field, value):
    updated_todo = context.response.json()
    if value == "finished":
        assert updated_todo['doneStatus'] == "true", (
            f"Expected doneStatus: true, but got: {updated_todo[field]}."
        )
    elif value == "not finished":
        assert updated_todo['doneStatus'] == "false", (
            f"Expected doneStatus: true, but got: {updated_todo[field]}."
        )
    else:
        assert updated_todo[field] == value, (
            f"Expected {value}: true, but got: {updated_todo[field]}."
        )


@given('there is no todo item with id "{id}"')
def step_impl(context, id):
    url = f"{context.api_url}/todos/{id}"
    response = requests.get(url)

    if response.status_code == 404:
        assert response.status_code == 404, (
            f"Validated: No todo item found with id '{id}'.")
    else:
        assert response.status_code == 404, (
            f"Expected no todo item with id '{id}', but found one with status {response.status_code}."
        )

    response = requests.get(f"{context.api_url}/todos")
    assert response.status_code == 200, "Failed to retrieve the full list of todos."

    context.initial_todos = response.json().get('todos', [])


@then('the system does not create or modify any todo items')
def step_impl(context):
    response = requests.get(f"{context.api_url}/todos")
    assert response.status_code == 200, "Failed to retrieve todos."

    current_todos = response.json().get('todos', [])

    initial_todos_json = json.dumps(context.initial_todos, indent=2)
    current_todos_json = json.dumps(current_todos, indent=2)

    if initial_todos_json != current_todos_json:
        diff = difflib.unified_diff(
            initial_todos_json.splitlines(),
            current_todos_json.splitlines(),
            fromfile='Initial Todos',
            tofile='Current Todos',
            lineterm=''
        )
        print(''.join(diff))
    assert current_todos == context.initial_todos, (
        "The system created or modified todo items unexpectedly."
    )


@when('the user sends a {method} request to "{endpoint}"')
def step_impl(context, method, endpoint):
    if ":id" in endpoint:
        if not hasattr(context, "todo_id"):
            todo_id = context.todo_created_responses[0].json().get('id')
            context.todo_id = todo_id
        endpoint = endpoint.replace(":id", str(context.todo_id))
    url = f"{context.api_url}" + endpoint
    if method == "GET":
        response = requests.get(url)
        context.response = response
        context.todos = response.json().get('todos', [])
    if method == "HEAD":
        response = requests.head(url)
        context.response = response
    if method == "DELETE":
        response = requests.delete(url)
        context.response = response


@when('the user sends a {method} request to "{endpoint}" as XML')
def step_impl(context, method, endpoint):
    if ":id" in endpoint:
        todo_id = context.todo_created_responses[0].json().get('id')
        endpoint = endpoint.replace(":id", str(todo_id))
    url = f"{context.api_url}" + endpoint
    if method == "GET":
        response = requests.get(url, headers={"Accept": "application/xml"})
        context.response = response
        context.todos = response.json().get('todos', [])
    if method == "HEAD":
        response = requests.head(url, headers={"Accept": "application/xml"})
        context.response = response


@then('the user get only 1 todo item')
def step_impl(context):
    print(context.todos)
    assert len(context.todos) == 1


@then('the user extract a todo id from todo item')
def step_impl(context):
    context.todo_id = context.todos[0].get('id')


@then('the response header "{header}" should be "{value}"')
def step_check_header(context, header, value):
    actual_value = context.response.headers.get(header)
    assert actual_value == value, (
        f"Expected {header} to be '{value}', but got '{actual_value}'"
    )


@then('the response should not have a body')
def step_check_no_body(context):
    assert not context.response.content, (
        f"Expected no body, but got content: {context.response.content}"
    )


@then('the response body contains an todo with the title "{expected_title}"')
def step_impl(context, expected_title):
    todo = context.todos[0]
    assert todo['title'] == expected_title, (
        f"Expected title: {expected_title}, but got: {todo['title']}."
    )


@then('the todo has a description of "{expected_description}"')
def step_impl(context, expected_description):
    todo = context.todos[0]
    assert todo['description'] == expected_description, (
        f"Expected description: {expected_description}, but got: {todo['description']}."
    )


@then('the done status is "{expected_doneStatus}"')
def step_impl(context, expected_doneStatus):
    todo = context.todos[0]
    actual_doneStatus = str(todo['doneStatus']).lower()
    assert actual_doneStatus == expected_doneStatus.lower(), (
        f"Expected done status: {expected_doneStatus}, but got: {actual_doneStatus}."
    )


@then('the system removes the todo item from the database')
def step_verify_todo_removal(context):
    endpoint = f"/todos/{context.todo_id}"
    url = f"{context.api_url}{endpoint}"

    response = requests.get(url)
    assert response.status_code == 404, (
        f"Expected 404, but got {response.status_code}. Todo was not removed."
    )
