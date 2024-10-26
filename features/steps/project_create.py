import requests
from behave import *

# Normal Flow
@when(u'the user sends a POST request to {endpoint} with the title {title}, completed {completed}, active {active}, and description {description}')
def step_impl(context, endpoint, title, completed, active, description):
    url = context.api_url + endpoint
    data = {
        "title": title,
        "completed": bool(completed),
        "active": bool(active),
        "description": description
    }
    
    res = requests.post(url, json=data)
    if res.status_code == 201:
        context.project_created_responses = []
        context.project_created_responses.append(res)

    context.res = res

@then(u'the project {title} should appear in the system')
def step_impl(context, title):
    response = requests.get(context.api_url + "/projects")
    assert context.res.status_code == 201 and title in str(response.json()['projects']), (
        f"Project {title} not found in the system"
    )

# Alternative Flow
@when(u'the user sends a POST request to {endpoint} with the title {title}')
def step_impl(context, endpoint, title):
    url = context.api_url + endpoint
    data = {
        "title": title
    }
    
    res = requests.post(url, json=data)
    if res.status_code == 201:
        context.project_created_responses = []
        context.project_created_responses.append(res)

    context.res = res

@then(u'the project {title} should not appear in the system')
def step_impl(context, title):
    response = requests.get(context.api_url + "/projects")
    assert context.res.status_code == 201 and title not in str(response.json()['projects']), (
        f"Project {title} found in the system"
    )

# Error Flow
@when(u'the user sends a POST request to /projects with the id {id}')
def step_impl(context, id):
    url = context.api_url + "/projects"
    data = {
        "id": id
    }
    
    context.res = requests.post(url, json=data)

@then(u'the system should respond with an error status code')
def step_impl(context):
    assert context.res.status_code == 400, (
        f"Expected status code 400 but got {context.res.status_code}"
    )