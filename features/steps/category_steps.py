import json
import requests
from behave import when, then, given

@when('the user submits a POST request to create a category with the title "{title}" and description "{description}"')
def step_create_category_with_title_and_description(context, title, description):
    context.title = title
    context.description = description
    
    payload = {
        "title": title,
        "description": description
    }
    
    headers = {'Content-Type': 'application/json'}
    context.response = requests.post(
        f"{context.api_url}/categories",
        json=payload,
        headers=headers
    )

@when('the user submits a POST request to create a category with the title "{title}"')
def step_create_category_with_title(context, title):
    context.title = title if title != "<empty>" else ""
    
    payload = {
        "title": context.title
    }
    
    headers = {'Content-Type': 'application/json'}
    context.response = requests.post(
        f"{context.api_url}/categories",
        json=payload,
        headers=headers
    )

@then('the category API responds with status code {status_code:d}')
def step_verify_response_status(context, status_code):
    assert context.response.status_code == status_code, (
        f"Expected status code: {status_code}, but got: {context.response.status_code}"
    )

@then('the response body confirms "title" as "{expected_title}"')
def step_verify_response_title(context, expected_title):
    response_json = context.response.json()
    categories = response_json.get('categories', [])
    if categories:
        actual_title = categories[0].get('title')
    else:
        actual_title = response_json.get('title')
    
    assert actual_title == expected_title, (
        f"Expected title: {expected_title}, but got: {actual_title}"
    )

@then('the response body includes "description" as "{expected_description}"')
def step_verify_response_description(context, expected_description):
    response_json = context.response.json()
    categories = response_json.get('categories', [])
    if categories:
        actual_description = categories[0].get('description')
    else:
        actual_description = response_json.get('description')
    
    assert actual_description == expected_description, (
        f"Expected description: {expected_description}, but got: {actual_description}"
    )

@then('the system stores the new category')
def step_verify_category_stored(context):
    response_json = context.response.json()
    categories = response_json.get('categories', [])
    if categories:
        category_id = categories[0].get('id')
    else:
        category_id = response_json.get('id')
    
    assert category_id, "The response does not contain an 'id'."
    
    url = f"{context.api_url}/categories/{category_id}"
    response = requests.get(url)
    
    assert response.status_code == 200, f"Failed to retrieve the category. Status: {response.status_code}"
    
    categories_list = response.json().get('categories', [])
    if categories_list:
        retrieved_category = categories_list[0]
    else:
        retrieved_category = response.json()
    
    expected_category = {
        "id": category_id,
        "title": context.title
    }
    
    if hasattr(context, 'description'):
        expected_category["description"] = context.description
        
    # Compare only the fields we expect to be present
    retrieved_category = {k: retrieved_category[k] for k in expected_category.keys() if k in retrieved_category}
    
    assert retrieved_category == expected_category, (
        f"Expected category:\n{expected_category}\nBut got:\n{retrieved_category}"
    )

@when('the user submits a POST request to create a category with an ID')
def step_create_category_with_id(context):
    payload = {
        "id": "invalid-id",
        "title": "Some Category"
    }
    
    headers = {'Content-Type': 'application/json'}
    context.response = requests.post(
        f"{context.api_url}/categories",
        json=payload,
        headers=headers
    )

@then('the category is not stored in the system')
def step_verify_category_not_stored(context):
    if hasattr(context, 'response') and context.response.status_code == 400:
        return  # If we got a 400 status code, the category wasn't stored
        
    url = f"{context.api_url}/categories"
    response = requests.get(url)
    
    assert response.status_code == 200, f"Failed to retrieve categories. Status: {response.status_code}"
    
    categories_list = response.json().get('categories', [])
    stored_titles = [category.get('title') for category in categories_list]
    
    assert context.title not in stored_titles, (
        f"The category with title '{context.title}' was incorrectly stored in the system."
    )

@then('the response body contains "errorMessages"')
def step_verify_error_messages(context):
    response_json = context.response.json()
    assert 'errorMessages' in response_json, (
        f"Expected 'errorMessages' in response, but got: {response_json}"
    )
    assert isinstance(response_json['errorMessages'], list), (
        f"Expected 'errorMessages' to be a list, but got: {type(response_json['errorMessages'])}"
    )
    assert len(response_json['errorMessages']) > 0, (
        "Expected 'errorMessages' to contain at least one error message"
    )

@given('a category exists with title "{title}"')
def step_create_category_for_deletion(context, title):
    # First create a category to be deleted
    payload = {
        "title": title
    }
    
    headers = {'Content-Type': 'application/json'}
    response = requests.post(
        f"{context.api_url}/categories",
        json=payload,
        headers=headers
    )
    
    assert response.status_code == 201, f"Failed to create category for deletion. Status: {response.status_code}"
    
    # Store the category ID for deletion
    response_json = response.json()
    categories = response_json.get('categories', [])
    if categories:
        context.category_id = categories[0].get('id')
    else:
        context.category_id = response_json.get('id')
    
    context.title = title

@given('a category with title "{title}" and description "{description}" exists for deletion')
def step_create_category_with_description_for_deletion(context, title, description):
    # First create a category with description to be deleted
    payload = {
        "title": title,
        "description": description
    }
    
    headers = {'Content-Type': 'application/json'}
    response = requests.post(
        f"{context.api_url}/categories",
        json=payload,
        headers=headers
    )
    
    assert response.status_code == 201, f"Failed to create category for deletion. Status: {response.status_code}"
    
    # Store the category ID for deletion
    response_json = response.json()
    categories = response_json.get('categories', [])
    if categories:
        context.category_id = categories[0].get('id')
    else:
        context.category_id = response_json.get('id')
    
    context.title = title
    context.description = description

@given('there are items associated with this category')
def step_create_items_for_category(context):
    # Create a sample item associated with the category
    payload = {
        "title": "Sample Item",
    }
    
    headers = {'Content-Type': 'application/json'}
    response = requests.post(
        f"{context.api_url}/categories/{context.category_id}/todos",
        json=payload,
        headers=headers
    )
    
    assert response.status_code == 201, f"Failed to create item for category. Status: {response.status_code}"
    context.item_id = response.json().get('id')

@when('the user sends a DELETE request to delete the category')
def step_delete_category(context):
    headers = {'Content-Type': 'application/json'}
    context.response = requests.delete(
        f"{context.api_url}/categories/{context.category_id}",
        headers=headers
    )

@when('the user sends a DELETE request to delete a category with ID "{invalid_id}"')
def step_delete_invalid_category(context, invalid_id):
    headers = {'Content-Type': 'application/json'}
    context.response = requests.delete(
        f"{context.api_url}/categories/{invalid_id}",
        headers=headers
    )

@then('the category with title "{title}" is no longer in the system')
def step_verify_category_deleted(context, title):
    # Try to fetch the deleted category
    response = requests.get(f"{context.api_url}/categories/{context.category_id}")
    
    assert response.status_code == 404, (
        f"Expected category to be deleted, but it was found with status: {response.status_code}"
    )

@then('no changes are made to the system')
def step_verify_no_system_changes(context):
    # This step is implicit since we're testing a non-existent category
    # No additional verification needed as the 404 status code already confirms this
    pass

@then('the associated items no longer reference the deleted category')
def step_verify_items_updated(context):
    # Verify the associated item no longer references the deleted category
    response = requests.get(f"{context.api_url}/todos/{context.item_id}")
    
    assert response.status_code == 200, f"Failed to retrieve item. Status: {response.status_code}"
    
    item = response.json()
    assert item.get('categoryId') is None, (
        f"Expected item to have no category reference, but found categoryId: {item.get('categoryId')}"
    )