Feature: View a Project by ID
  As a user, I want to view specific details of a project by ID.

  Background:
    Given the project management API is running

  Scenario Outline: User retrieves a project by ID (Normal Flow)
    Given a project with ID "<id>" and title "Detailed Project" exists
    When the user submits a GET request to /projects/<id>
    Then the project API responds with status code 200
    And the response body confirms "id" as "<id>" and "title" as "Detailed Project"

    Examples:
      | id |
      | 1  |
      | 2  |

  Scenario: User attempts to retrieve a project with missing ID (Alternate Flow)
    When the user submits a GET request to /projects/ without specifying an ID
    Then the project API responds with status code 400
    And the response body contains "errorMessages" for "Invalid project ID"

  Scenario: User attempts to retrieve a project with an invalid ID (Error Flow)
    When the user submits a GET request to /projects/-1
    Then the project API responds with status code 400
    And the response body contains "errorMessages" for "Invalid project ID"
