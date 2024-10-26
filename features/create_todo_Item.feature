Feature: Create a New Todo Item
  As a user, I want to create a new todo item, so that I can keep track of tasks I need to complete.

 Background:
    Given the todo management API is running

  Scenario Outline: User creates a new todo item successfully (Normal Flow)
    When the user sends a POST request to /todos with the title "<title>"
    Then the API responds with status code 201 (Created)
    And the response body contains "title" of "<title>"
    Then the system saves the todo item

  Examples:
    | title  |
    | task 1 |
    | task 2 |
    | task 3 |
    | task 4 |

  Scenario Outline: User creates a new todo item with description (Alternative Flow)
    When the user sends a POST request to /todos with the title name "<title>" and description "<description>"
    Then the API responds with status code 201 (Created)
    And the response body contains "title" of "<title>"
    Then the system saves the todo item

  Examples:
    | title  | description             |
    | task 1 | "This is description 1" |
    | task 2 | "This is description 2" |
    | task 3 | "This is description 3" |
    | task 4 | "This is description 4" |

  Scenario: The user attempts to create a new todo item without entering the title (Error Flow)
    When the user sends a POST request to /todos with the title "<empty>"
    Then the API responds with status code 400 (Bad Request)
    And the response body contains "errorMessages" of "Failed Validation: title : can not be empty"
    And the todo item is not stored in the system