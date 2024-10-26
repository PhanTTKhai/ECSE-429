from behave import given, when, then
import requests

@when('the user sends a GET request to "{endpoint}"')
def step_impl(context, endpoint):
    url = f"{context.api_url}" + endpoint
    response = requests.get(url)
    context.response = response
    context.todos = response.json().get('todos', [])


@then('the response body contains an todo with the title "{expected_title}"')
def step_impl(context, expected_title):
    todo = context.todos[0]
    assert todo['title'] == expected_title, (
        f"Expected title: {expected_title}, but got: {todo['title']}."
    )
    print(f"Validated: Todo title is '{todo['title']}'.")


@then('the todo has a description of "{expected_description}"')
def step_impl(context, expected_description):
    todo = context.todos[0]
    assert todo['description'] == expected_description, (
        f"Expected description: {expected_description}, but got: {todo['description']}."
    )
    print(f"Validated: Todo description is '{todo['description']}'.")


@then('the done status is "{expected_doneStatus}"')
def step_impl(context, expected_doneStatus):
    todo = context.todos[0]
    actual_doneStatus = str(todo['doneStatus']).lower()
    assert actual_doneStatus == expected_doneStatus.lower(), (
        f"Expected done status: {expected_doneStatus}, but got: {actual_doneStatus}."
    )
    print(f"Validated: Todo done status is '{actual_doneStatus}'.")