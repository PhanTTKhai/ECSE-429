Feature: Update Todo Item Details
  As a user, I want to edit the details of a todo item so that I can keep my task list accurate and up-to-date with my current needs.

  Background:
    Given the todo management API is running

  Scenario Outline: The user successfully update a todo item details with PUT method.
    Given there are todo items stored in the system
      | title   | doneStatus   | description   |
      | <title> | <doneStatus> | <description> |
    When the user update the "<field>" of todo task "some task" to "<value>" with PUT
    Then the API responds with status code 200 (OK)
    And the system updates the todo item "<field>" to "<value>"

    Examples:
      | title     | doneStatus | description | field       | value        |
      | some task | false      | ""          | doneStatus  | finished     |
      | some task | false      | ""          | title       | new title    |
      | some task | false      | ""          | description | it is a task |

  Scenario Outline: The user successfully update a todo item details with POST method.
    Given there are todo items stored in the system
      | title   | doneStatus   | description   |
      | <title> | <doneStatus> | <description> |
    When the user update the "<field>" of todo task "some task" to "<value>" with POST
    Then the API responds with status code 200 (OK)
    And the system updates the todo item "<field>" to "<value>"

    Examples:
      | title     | doneStatus | description | field       | value        |
      | some task | false      | ""          | doneStatus  | finished     |
      | some task | false      | ""          | title       | new title    |
      | some task | false      | ""          | description | it is a task |

  Scenario Outline: User tries to mark a non-existent todo item as finished.
    Given there is no todo item with id "<todo_id>"
    When the user update the todo task with id "<todo_id>" as "finished"
    Then the API responds with status code 404 (Not Found)
    Then the system does not create or modify any todo items

    Examples:
      | todo_id |
      | 0       |
      | -1      |
      | -2      |
      | -3      |