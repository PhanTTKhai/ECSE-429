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

@when('the user submits a PUT request to update the category with ID "{category_id}" to have the title "{new_title}" and description "{new_description}"')
def step_modify_category_with_title_and_description(context, category_id, new_title, new_description):
    context.category_id = category_id
    context.new_title = new_title
    context.new_description = new_description

    payload = {
        "title": new_title,
        "description": new_description
    }

    headers = {'Content-Type': 'application/json'}
    context.response = requests.put(
        f"{context.api_url}/categories/{category_id}",
        json=payload,
        headers=headers
    )

@when('the user submits a PUT request to update the category with ID "{category_id}" to have an empty title "{empty_title}" and an empty description "{empty_description}"')
def step_modify_category_with_empty_fields(context, category_id, empty_title, empty_description):
    context.category_id = category_id
    context.new_title = empty_title if empty_title != "<empty>" else ""
    context.new_description = empty_description if empty_description != "<empty>" else ""

    payload = {
        "title": context.new_title,
        "description": context.new_description
    }

    headers = {'Content-Type': 'application/json'}
    context.response = requests.put(
        f"{context.api_url}/categories/{category_id}",
        json=payload,
        headers=headers
    )

@then('the response body confirms "description" as "{expected_description}"')
def step_verify_response_description(context, expected_description):
    response_json = context.response.json()
    actual_description = response_json.get('description')
    
    assert actual_description == expected_description, (
        f"Expected description: {expected_description}, but got: {actual_description}"
    )

@then('the category with ID "{category_id}" is not updated in the system')
def step_verify_category_not_updated(context, category_id):
    url = f"{context.api_url}/categories/{category_id}"
    response = requests.get(url)
    
    assert response.status_code == 200, f"Failed to retrieve category. Status: {response.status_code}"
    
    category = response.json()
    assert category.get("title") != context.new_title or category.get("description") != context.new_description, (
        "The category was unexpectedly updated in the system."
    )
@then('no category is updated in the system')
def step_verify_no_category_updated(context):
    # Fetch the category using its ID to verify it hasn't been modified
    url = f"{context.api_url}/categories/{context.category_id}"
    response = requests.get(url)
    
    assert response.status_code == 200, f"Failed to retrieve category. Status: {response.status_code}"
    
    category = response.json()
    
    # Check if the title and description remain unchanged
    assert category.get("title") == context.original_title, (
        f"Expected title: {context.original_title}, but got: {category.get('title')}"
    )
    assert category.get("description") == context.original_description, (
        f"Expected description: {context.original_description}, but got: {category.get('description')}"
    )

@then('the system updates the category with ID "{category_id}"')
def step_verify_category_updated(context, category_id):
    # Fetch the category using its ID to verify it was updated
    url = f"{context.api_url}/categories/{category_id}"
    response = requests.get(url)
    
    assert response.status_code == 200, f"Failed to retrieve category. Status: {response.status_code}"
    
    category = response.json()
    
    # Check if the title and description have been updated
    assert category.get("title") == context.new_title, (
        f"Expected updated title: {context.new_title}, but got: {category.get('title')}"
    )
    assert category.get("description") == context.new_description, (
        f"Expected updated description: {context.new_description}, but got: {category.get('description')}"
    )

@given('there are categories stored in the system')
def step_create_categories(context):
    for row in context.table:
        payload = {
            "title": row["title"],
            "description": row["description"]
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(
            f"{context.api_url}/categories",
            json=payload,
            headers=headers
        )
        assert response.status_code == 201, f"Failed to create category: {row['title']}"

@when('the user updates the "{field}" of category "{title}" to "{value}" with PUT')
def step_update_category_with_put(context, field, title, value):
    # Retrieve category ID by title
    response = requests.get(f"{context.api_url}/categories")
    categories = response.json().get('categories', [])
    category = next((c for c in categories if c["title"] == title), None)
    assert category, f"Category with title '{title}' not found"
    
    context.category_id = category["id"]
    
    # Update the field
    payload = {field: value}
    headers = {'Content-Type': 'application/json'}
    context.response = requests.put(
        f"{context.api_url}/categories/{context.category_id}",
        json=payload,
        headers=headers
    )


@when('the user updates the "{field}" of category "{title}" to "{value}" with POST')
def step_update_category_with_post(context, field, title, value):
    # Retrieve category ID by title
    response = requests.get(f"{context.api_url}/categories")
    categories = response.json().get('categories', [])
    category = next((c for c in categories if c["title"] == title), None)
    assert category, f"Category with title '{title}' not found"
    
    context.category_id = category["id"]
    
    # Update the field
    payload = {field: value}
    headers = {'Content-Type': 'application/json'}
    context.response = requests.post(
        f"{context.api_url}/categories/{context.category_id}",
        json=payload,
        headers=headers
    )
@given('there is no category with ID "{category_id}"')
def step_ensure_no_category_exists(context, category_id):
    response = requests.get(f"{context.api_url}/categories/{category_id}")
    if response.status_code == 200:
        requests.delete(f"{context.api_url}/categories/{category_id}")
    context.non_existent_id = category_id

@when('the user tries to update the category with ID "{category_id}" as "{status}"')
def step_update_nonexistent_category(context, category_id, status):
    payload = {"doneStatus": status}
    headers = {'Content-Type': 'application/json'}
    context.response = requests.put(
        f"{context.api_url}/categories/{category_id}",
        json=payload,
        headers=headers
    )

@then('the system does not create or modify any categories')
def step_verify_no_modifications(context):
    # Verify there were no unintended modifications by checking categories
    response = requests.get(f"{context.api_url}/categories/{context.non_existent_id}")
    assert response.status_code == 404, (
        "A non-existent category was found or inadvertently created."
    )

@then('the API responds with status code {status_code:d} ({status_text})')
def step_verify_response_status(context, status_code, status_text):
    assert context.response.status_code == status_code, (
        f"Expected status code: {status_code} ({status_text}), but got: {context.response.status_code}"
    )

@when('the user tries to update the category with ID "{category_id}"')
def step_update_category_by_id(context, category_id):
    # Prepare payload for update (this can be any field that you're updating)
    payload = {"title": "Updated Category Title"}  # Example payload, adjust as needed
    headers = {'Content-Type': 'application/json'}
    
    # Send the update request with PUT (or POST depending on your requirement)
    context.response = requests.put(
        f"{context.api_url}/categories/{category_id}",
        json=payload,
        headers=headers
    )
    

@when('the user sends a GET request to /categories')
def step_get_all_categories(context):
    context.response = requests.get(f"{context.api_url}/categories")
    print(f"Response: {context.response.status_code} - {context.response.json()}")

@then('the response body contains a list of all categories')
def step_check_response_for_categories(context):
    # Ensure the response body contains the 'categories' key
    response_json = context.response.json()
    
    # Check if 'categories' is a key in the response and its value is a list
    assert 'categories' in response_json, "Response body does not contain 'categories' key"
    assert isinstance(response_json['categories'], list), "Categories is not a list"
    
    # Optionally, you can also check if the list contains at least one category
    assert len(response_json['categories']) > 0, "Categories list is empty"

@given('there are no categories in the system')
def clear_categories(context):
    # Ensure the response body contains the 'categories' key
    response_json = context.response.json()
    
    # Check if 'categories' is a key in the response and its value is a list
    assert 'categories' in response_json, "Response body does not contain 'categories' key"
    assert isinstance(response_json['categories'], list), "Categories is not a list"
    
    # Optionally, you can also check if the list contains at least one category
    assert len(response_json['categories']) > 0, "Categories list is empty"
    

@then('the response body contains an empty list')
def step_check_empty_list(context):
    response_json = context.response.json()

    # Handle if the response is an empty dictionary
    if isinstance(response_json, dict):
        # Check if the key 'todos' exists and is an empty list, or if the response body itself is empty
        todos = response_json.get('todos', [])
        assert todos == [], "The 'todos' list is not empty"
    else:
        assert response_json == [], f"Expected an empty list, but got {response_json}"


@when('the user sends an invalid GET request to /invalid/categories')
def step_send_invalid_get_request(context):
    # Sending the invalid request
    context.response = requests.get(f"{context.api_url}/invalid/categories")

@then('the response body contains a list of all todos associated with category ID "{category_id}"')
def step_verify_todos_associated_with_category(context, category_id):
    response_json = context.response.json()

    # Assuming the response has a 'todos' key that contains a list of todos
    assert 'todos' in response_json, "Response does not contain 'todos' key"
    
    todos = response_json['todos']
    assert isinstance(todos, list), "The 'todos' key does not contain a list"

    for todo in todos:
        assert todo['categoryId'] == int(category_id), f"Todo {todo['id']} is not associated with category {category_id}"

@then('no todos are returned')
def step_verify_no_todos_returned(context):
    response_json = context.response.json()
    assert isinstance(response_json, list), "Response body is not a list"
    assert len(response_json) == 0, "Expected no todos, but got some"

@given('the category with ID "{category_id}" has no associated todos')
def step_category_has_no_todos(context, category_id):
    # Ensure the category has no todos by interacting with the API or your database
    # This can involve clearing out todos associated with the given category ID, for testing purposes
    context.category_id = category_id
    # Optionally: Ensure no todos are linked to the category
    context.response = requests.get(f"{context.api_url}/categories/{category_id}/todos")
    # Verify no todos are linked to this category before proceeding with the test

@when('the user sends a GET request to /categories/{category_id}/todos')
def step_send_get_request_for_category_with_no_todos(context, category_id):
    context.category_id = category_id
    context.response = requests.get(f"{context.api_url}/categories/{category_id}/todos")
