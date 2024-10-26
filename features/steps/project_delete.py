import requests
from behave import *

@given(u'the system is running and a project with title {title} exists')
def step_impl(context, title):
    url = context.api_url + "/projects"
    
    res = requests.post(url, json={"title": title})
    if res.status_code == 201:
        context.id = res.json().get('id')
        # context.project_created_responses = []
        # context.project_created_responses.append(res)

# Normal Flow
@when(u'the user deletes the project with title {title}')
def step_impl(context, title):
    url = context.api_url + "/projects/" + context.id
    context.res = requests.delete(url)

@then(u'the project with title {title} should be deleted from the system')
def step_impl(context, title):
    response = requests.get(context.api_url + "/projects")
    assert context.res.status_code == 200 and title not in str(response.json()['projects']), (
        f"Project {title} found in the system"
    )

# Alternate flow
@when(u'the user updates the project with title {title} as with field completed {completed}')
def step_impl(context, title, completed):
    url = context.api_url + "/projects/" + context.id
    context.res = requests.post(url, json={"completed": bool(completed)})
    assert context.res.status_code == 200, (
        f"Project {title} not updated"
    )

@then(u'the project with title {title} should be marked as completed')
def step_impl(context, title):
    response = requests.get(context.api_url + "/projects/" + context.id)
    if response.status_code == 200:
        isCompleted = response.json().get('projects')[0].get('completed')
        assert bool(isCompleted), (
            f"Project {title} not marked as completed {isCompleted}"
        )

# Error flow
@given(u'the system is running and there is no project with id {id}')
def step_impl(context, id):
    url = context.api_url + "/projects/" + id
    res = requests.get(url)
    assert res.status_code == 404

@when(u'the user sends a DELETE request to {endpoint}/{id}')
def step_impl(context, endpoint, id):
    url = context.api_url + endpoint + "/" + id
    context.num_projects_before_invalid_delete = len(requests.get(context.api_url + "/projects").json().get('projects'))
    context.res = requests.delete(url)
    context.num_projects_after_invalid_delete = len(requests.get(context.api_url + "/projects").json().get('projects'))

@then(u'the system should respond with an error status code and no project should be deleted')
def step_impl(context):
    assert context.res.status_code == 404 and context.num_projects_before_invalid_delete == context.num_projects_after_invalid_delete