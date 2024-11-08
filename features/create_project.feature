Feature: Create a New Project
  As a user, I want to create a new project so that I can manage my tasks effectively.

  Background:
    Given the todo management API is running

  Scenario Outline: User creates a new project with a specific ID (Normal Flow)
    When the user submits a POST request to /projects with ID "<id>" and title "<title>"
    Then the project API responds with status code 201
    And the response body confirms "id" as "<id>" and "title" as "<title>"
    Then the system stores the new project

    Examples:
      | id | title       |
      | 1  | Project A   |
      | 2  | Project B   |
      | 3  | Project C   |

  Scenario Outline: User creates a new project without specifying an ID (Alternate Flow)
    When the user submits a POST request to /projects with title "<title>" and description "<description>"
    Then the project API responds with status code 201
    And the response body confirms "title" as "<title>" and "description" as "<description>"
    Then the system stores the new project

    Examples:
      | title      | description         |
      | Project X  | Description X       |
      | Project Y  | Description Y       |
      | Project Z  | Description Z       |

  Scenario: User attempts to create a project with an invalid ID (Error Flow)
    When the user submits a POST request to /projects with an invalid ID "-1" and title "Invalid Project"
    Then the project API responds with status code 400
    And the response body contains "errorMessages" for "Invalid project ID"
    And the project is not stored in the system
