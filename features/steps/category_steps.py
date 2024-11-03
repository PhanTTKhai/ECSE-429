import json
import requests
from behave import given, when, then

@then('the API responds with status code {status_code:d} ({status_text})')
def step_then_check_status_code(context, status_code, status_text):
    assert context.response.status_code == status_code, (
        f"Expected status code {status_code}, but got {context.response.status_code}."
    )

@then('the system saves the category')
def step_then_system_saves_category(context):
    # Validate that the category is stored correctly in the system
    category_id = context.response.json().get('id')
    assert category_id, "The response does not contain an 'id'."

    response = requests.get(f"{context.api_url}/categories/{category_id}")
    assert response.status_code == 200, f"Failed to retrieve the category. Status code: {response.status_code}"

    retrieved_category = response.json()
    
    # Extract the first category from the 'categories' list
    retrieved_category = retrieved_category.get('categories', [{}])[0]
    
    expected_category = {
        "id": category_id,
        "title": context.title,  # Use context.title set during category creation
        "description": context.description,  # Use context.description set during category creation
    }

    assert retrieved_category == expected_category, (
        f"Expected category:\n{expected_category}\nBut got:\n{retrieved_category}"
    )

@when('the user sends a POST request to {endpoint} with the title "{title}" and description "{description}"')
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
        context.categories = []
        context.categories.append(response)

    context.response = response

@then('the response body contains "title" of "{title}"')
def step_then_check_response_title(context, title):
    response_data = context.response.json()
    assert response_data.get("title") == title, (
        f"Expected title '{title}', but got '{response_data.get('title')}'."
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
    url = f"{context.api_url}/categories"
    response = requests.get(url)
    print(response)

    assert response.status_code == 200, f"Failed to retrieve the category items. Status code: {response.status_code}"

    # Assuming the response structure contains a list of categories under a key 'categories'
    categories = response.json().get('categories', []) 
    print(categories)

    # Extract the titles of the stored categories
    stored_titles = [category.get('title') for category in categories]

    assert context.title not in stored_titles, (
        f"The category item with title '{context.title}' was incorrectly stored in the system."
    )
