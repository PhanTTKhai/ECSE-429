Feature: View All Todos
  As a user, I want to retrieve all tasks associated with a specific todo item or project, so that I can see what needs to be done for that item or project.

  Background:
    Given the todo management API is running

  Scenario: User retrieves all todo items successfully
    Given there are todo items stored in the system
      | title         | doneStatus | description  |
      | Buy groceries | false      | Necessity    |
      | Finish report | true       | Work project |
    When the user sends a GET request to "/todos"
    Then the API responds with status code 200 (OK)

  Scenario Outline: User retrieve todo items with a specific title
    Given there are todo items stored in the system
      | title         | doneStatus | description  |
      | some task     | true       | my task      |
      | Buy groceries | false      | Necessity    |
      | Finish report | true       | Work project |
    When the user sends a GET request to "/todos?<filter>"
    Then the response body contains an todo with the title "<title>"
    And the todo has a description of "my task"
    And the done status is "true"

    Examples:
      | filter                | title     |
      | title=some%20task     | some task |
      | description=my%20task | some task |

  Scenario Outline: User provides invalid query parameter while listing todos
    Given there are todo items stored in the system
      | title         | doneStatus | description  |
      | some task     | true       | my task      |
      | Buy groceries | false      | Necessity    |
      | Finish report | true       | Work project |
    Given the todo management API is running
    When the user sends a GET request to "/todos?<filter>"
    Then the API responds with status code 400 (Bad Request)

    Examples:
      | filter         |
      | finished=true  |
      | name=my%20task |

  Scenario Outline: User provides invalid query parameter value while listing todos
    Given there are todo items stored in the system
      | title         | doneStatus | description  |
      | some task     | true       | my task      |
      | Buy groceries | false      | Necessity    |
      | Finish report | true       | Work project |
    Given the todo management API is running
    When the user sends a GET request to "/todos?<filter>"
    Then the API responds with status code 400 (Bad Request)

    Examples:
      | filter             |
      | doneStatus=maybeee |

