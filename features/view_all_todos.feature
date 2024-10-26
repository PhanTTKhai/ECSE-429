Feature: View All Todos
  As a user, I want to retrieve all tasks associated with a specific todo item or project, so that I can see what needs to be done for that item or project.

  Background:
    Given the todo management API is running
    And there are todo items stored in the system
      | title          | doneStatus | description   |
      | Buy groceries  | false      | Necessity     |
      | Finish report  | true       | Work project  |

  Scenario: User retrieves all todo items successfully
    When the user sends a GET request to "/todos"
    Then the API responds with status code 200 (OK)

  Scenario: User retrieve todo items with a specific title
    When the user sends a GET request to "/todos?title=Buy%20groceries"
    Then the response body contains an todo with the title "Buy groceries"
    And the todo has a description of "Necessity"
    And the done status is "false"

#  Scenario: User provides invalid query parameter while listing todos
#    Given the todo management API is running
#    When the user sends a GET request to "/todos?doneStatus=maybe"
#    Then the API responds with status code 400 (Bad Request)
#
#  Scenario: User provides invalid query parameter value while listing todos
#    Given the todo management API is running
#    When the user sends a GET request to "/todos?doneStatus=maybe"
#    Then the API responds with status code 400 (Bad Request)


