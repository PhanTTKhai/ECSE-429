Feature: Retrieve Project Details
  As a user, I want to retrieve details of specific projects to view their information.

  Background:
    Given the todo management API is running

  Scenario Outline: User retrieves an existing project by ID (Normal Flow)
    Given a project with ID "<id>" and title "<title>" exists
    When the user submits a GET request to /projects/<id>
    Then the project API responds with status code 200
    And the response body confirms "id" as "<id>" and "title" as "<title>"

    Examples:
      | id | title      |
      | 1  | Project A  |
      | 2  | Project B  |

  Scenario: User retrieves a project when no projects exist (Alternate Flow)
    Given no projects exist
    When the user submits a GET request to /projects/1
    Then the project API responds with status code 404
    And the response body contains "errorMessages" for "Project not found"

  Scenario: User attempts to retrieve a project with an invalid ID (Error Flow)
    When the user submits a GET request to /projects/-1
    Then the project API responds with status code 400
    And the response body contains "errorMessages" for "Invalid project ID"
