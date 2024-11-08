import requests


def before_all(context):
    context.api_url = 'http://localhost:4567'  # Replace with your actual API URL
    print("Checking if the API is running...")

    try:
        response = requests.get(f"{context.api_url}/docs")
        assert response.status_code == 200, "API is not responding with status 200"
        print("API is running.")
    except (requests.ConnectionError, AssertionError) as e:
        raise RuntimeError(f"Stopping tests: API is unavailable: {str(e)}")


def after_scenario(context, scenario):
    if hasattr(context, 'todo_created_responses'):
        for todo in context.todo_created_responses:
            todo_id = todo.json().get('id')
            response = requests.delete(f"{context.api_url}/todos/{todo_id}")
            if response.status_code in [200, 204]:
                print(f"Deleted todo with ID: {todo_id}")
            else:
                print(f"Failed to delete todo with ID: {todo_id}. Status: {response.status_code}")
    
    # Cleanup created categories
    if hasattr(context, 'category_created_responses'):
        for category in context.category_created_responses:
            category_id = category.json().get('id')
            response = requests.delete(f"{context.api_url}/categories/{category_id}")
            if response.status_code in [200, 204]:
                print(f"Deleted category with ID: {category_id}")
            else:
                print(f"Failed to delete category with ID: {category_id}. Status: {response.status_code}")