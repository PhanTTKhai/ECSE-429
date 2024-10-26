Feature: Mark Todo as Finished
  As a user, I want to mark a todo item as finished, so that I can track what tasks I've finished

  Background:
    Given the todo management API is running
    And there are todo items stored in the system
      | title              | doneStatus | description   |
      | Not finished todo  | false      | Necessity     |

  Scenario: The user successfully marks a todo item as finished by updating its status with PUT method.
    When the user update the todo task "Not finished todo" as "finished"
    Then the API responds with status code 200 (OK)
    And the system updates the todo item "doneStatus" to "finished"

  Scenario: The user successfully marks a todo item as not finished by updating its status with PUT method.
    When the user update the todo task "Not finished todo" as "not finished"
    Then the API responds with status code 200 (OK)
    And the system updates the todo item "doneStatus" to "not finished"

  Scenario: User tries to mark a non-existent todo item as finished.
    Given there is no todo item with id "-1"
    When the user update the todo task with id "-1" as "finished"
    Then the API responds with status code 404 (Not Found)
    Then the system does not create or modify any todo items