Feature: Edit Todo Description
  As a user, I want to send a HEAD request to todo, so that I can quickly see the todo details.

  Background:
    Given the todo management API is running

  Scenario Outline: The user retrieve HEAD for a todo instance
    Given there are todo items stored in the system
      | title   | doneStatus   | description   |
      | <title> | <doneStatus> | <description> |
    When the user sends a HEAD request to "/todos/:id"
    Then the API responds with status code 200 (OK)
    And the response should not have a body
    And the response header "Content-Type" should be "application/json"

    Examples:
      | title  | doneStatus | description             |
      | task 1 | false      | "This is description 1" |
      | task 2 | true       | "This is description 2" |
      | task 3 | true       | ""                      |
      | task 4 | false      | ""                      |

  Scenario Outline: The user retrieve HEAD for a todo instance as XML
    Given there are todo items stored in the system
      | title   | doneStatus   | description   |
      | <title> | <doneStatus> | <description> |
    When the user sends a HEAD request to "/todos/:id" as XML
    Then the API responds with status code 200 (OK)
    And the response should not have a body
    And the response header "Content-Type" should be "application/xml"

    Examples:
      | title  | doneStatus | description             |
      | task 1 | false      | "This is description 1" |
      | task 2 | true       | "This is description 2" |
      | task 3 | true       | ""                      |
      | task 4 | false      | ""                      |

  Scenario Outline: Send a HEAD request for a non-existing todo
    Given there is no todo item with id "<todo_id>"
    When the user sends a HEAD request to "/todos/0"
    Then the API responds with status code 404 (Not Found)
    And the response should not have a body
    Then the system does not create or modify any todo items

    Examples:
      | todo_id |
      | 0       |
      | -1      |
      | -2      |
      | -3      |