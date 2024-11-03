import json
import requests
from behave import given, when, then

# @when('the user sends a POST request to {endpoint} with the title "{title}"')
# def step_when_user_creates_category(context, endpoint, title):
#     context.endpoint = endpoint
#     payload = {
#         "title": title
#     }

#     headers = {'Content-Type': 'application/json'}
#     response = requests.post(f"{context.api_url}{endpoint}", json=payload, headers=headers)

#     context.response = response

@then('the API responds with status code {status_code:d} ({status_text})')
def step_then_check_status_code(context, status_code, status_text):
    assert context.response.status_code == status_code, (
        f"Expected status code {status_code}, but got {context.response.status_code}."
    )

@then('the response body contains "title" of "{title}"')
def step_then_check_response_title(context, title):
    response_data = context.response.json()
    assert response_data.get("title") == title, (
        f"Expected title '{title}', but got '{response_data.get('title')}'."
    )

@then('the system saves the category')
def step_then_system_saves_category(context):
    # Validate that the category is stored correctly in the system
    category_id = context.response.json().get('id')
    assert category_id, "The response does not contain an 'id'."

    response = requests.get(f"{context.api_url}/categories/{category_id}")
    assert response.status_code == 200, f"Failed to retrieve the category. Status code: {response.status_code}"

    retrieved_category = response.json()
    expected_category = {
        "id": category_id,
        "title": context.response.json().get("title"),
    }
    
    assert retrieved_category == expected_category, (
        f"Expected category:\n{expected_category}\nBut got:\n{retrieved_category}"
    )

@when('the user sends a POST request to {endpoint} with the name "{name}" and description "{description}"')
def step_when_user_creates_category_with_description(context, endpoint, name, description):
    payload = {
        "name": name,
        "description": description
    }

    headers = {'Content-Type': 'application/json'}
    response = requests.post(f"{context.api_url}{endpoint}", json=payload, headers=headers)

    context.response = response

@then('the response body contains "name" of "{name}"')
def step_then_check_response_name(context, name):
    response_data = context.response.json()
    assert response_data.get("name") == name, (
        f"Expected name '{name}', but got '{response_data.get('name')}'."
    )

@when('the user sends a POST request to {endpoint} with an ID')
def step_when_user_creates_category_with_id(context, endpoint):
    payload = {
        "id": 1  # or any ID that would cause an error
    }
    
    headers = {'Content-Type': 'application/json'}
    context.response = requests.post(f"{context.api_url}{endpoint}", json=payload, headers=headers)

@then('the response body contains "errorMessages"')
def step_then_check_error_messages(context):
    response_data = context.response.json()
    assert "errorMessages" in response_data, "Expected 'errorMessages' in the response body."

@then('the category is not stored in the system')
def step_then_category_is_not_stored(context):
    category_id = context.response.json().get('id')
    assert category_id, "The response does not contain an 'id'."
    
    response = requests.get(f"{context.api_url}/categories/{category_id}")
    assert response.status_code == 404, (
        f"Expected 404, but got {response.status_code}. Category was not removed."
    )
