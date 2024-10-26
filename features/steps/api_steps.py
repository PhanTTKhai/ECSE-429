from behave import given, then
import requests

@given(u'the todo management API is running')
def step_impl(context):
    context.api_url = 'http://localhost:4567'

@given('there are todo items stored in the system')
def step_impl(context):
    """
    Create todo items from the Gherkin table via POST requests.
    """
    headers = {'Content-Type': 'application/json'}
    context.todo_created_responses = []
    for row in context.table:
        # Prepare the payload for the POST request
        payload = {
            'title': row['title'],
            'doneStatus': row['doneStatus'].lower() == 'true',  # Convert to boolean
            'description': row['description']
        }

        # Send the POST request to create the todo item
        response = requests.post(f"{context.api_url}/todos", json=payload, headers=headers)

        # Verify the request was successful
        assert response.status_code == 201, (
            f"Failed to create todo: {row['title']}. Status: {response.status_code}"
        )
        context.todo_created_responses.append(response)

        # Print success message
        print(f"Created todo: {row['title']}")

@then('the API responds with status code {status_code:d} ({status_message})')
def step_impl(context, status_code, status_message):
    if not hasattr(context, 'response'):
        raise AttributeError("No response found in the context. Make sure the POST request was successful.")

    actual_status_code = context.response.status_code
    assert actual_status_code == status_code, (
        f"Expected status code {status_code}, but got {actual_status_code}."
    )

    print(f"API responded with status code: {actual_status_code} ({status_message})")