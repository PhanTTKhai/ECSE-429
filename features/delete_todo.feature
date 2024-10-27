Feature:  Delete Todo Item
  As a user, I want to delete a todo item, so that I can remove tasks that are no longer relevant.

  Background:
    Given the todo management API is running

  Scenario Outline: User deletes a todo item successfully
    Given there are todo items stored in the system
      | title   | doneStatus   | description   |
      | <title> | <doneStatus> | <description> |
    When the user sends a DELETE request to "/todos/:id"
    Then the API responds with status code 200 (OK)
    And the system removes the todo item from the database

    Examples:
      | title  | doneStatus | description             |
      | task 1 | false      | "This is description 1" |
      | task 2 | true       | "This is description 2" |
      | task 3 | true       | ""                      |
      | task 4 | false      | ""                      |


  Scenario Outline: The user deletes a todo item with a todo filter.
    Given there are todo items stored in the system
      | title     | doneStatus | description |
      | some task | true       | "my task"   |
    When the user sends a GET request to "/todos?<filter>"
    Then the user get only 1 todo item
    And the user extract a todo id from todo item
    When the user sends a DELETE request to "/todos/:id"
    Then the API responds with status code 200 (OK)
    And the system removes the todo item from the database

    Examples:
      | filter                  |
      | title=some%20task       |
      | description="my%20task" |

  Scenario Outline: The user attempts to delete a todo item that does not exist.
    Given there is no todo item with id "<todo_id>"
    When the user sends a DELETE request to "/todos/:-1"
    Then the API responds with status code 404 (Not Found)
    Then the system does not create or modify any todo items

    Examples:
      | todo_id |
      | 0       |
      | -1      |
      | -2      |
      | -3      |