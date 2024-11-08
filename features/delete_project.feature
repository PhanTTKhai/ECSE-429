Feature: Delete a Project
  As a user, I want to delete projects that are no longer needed.

  Background:
    Given the todo management API is running

  Scenario: User deletes an existing project by ID (Normal Flow)
    Given a project with ID "<id>" and title "Project to Delete" exists
    When the user submits a DELETE request to /projects/<id>
    Then the project API responds with status code 204
    And the project is not stored in the system

    Examples:
      | id |
      | 1  |

  Scenario: User attempts to delete a project with a missing ID (Alternate Flow) 
    When the user submits a DELETE request to /projects/ without specifying an ID
    Then the project API responds with status code 400
    And the response body contains "errorMessages" for "Invalid project ID"

  Scenario: User attempts to delete a project with an invalid ID (Error Flow)
    When the user submits a DELETE request to /projects/-1
    Then the project API responds with status code 400
    And the response body contains "errorMessages" for "Invalid project ID"
