from behave import given, then


@given(u'the todo management API is running')
def step_impl(context):
    context.api_url = 'http://localhost:4567'


@then('the API responds with status code {status_code:d} ({status_message})')
def step_impl(context, status_code, status_message):
    if not hasattr(context, 'response'):
        raise AttributeError("No response found in the context. Make sure the POST request was successful.")

    actual_status_code = context.response.status_code
    assert actual_status_code == status_code, (
        f"Expected status code {status_code}, but got {actual_status_code}."
    )
