Feature: Update a Project
  As a user, I want to update details of a project to keep information current.

  Background:
    Given the project management API is running

  Scenario Outline: User updates a project with a POST request (Normal Flow)
    Given a project with ID "<id>" and title "Project to Update" exists
    When the user submits a POST request to /projects/<id> with a new title "Updated Project"
    Then the project API responds with status code 200
    And the response body confirms "title" as "Updated Project"
    And the system updates the project

    Examples:
      | id |
      | 1  |

  Scenario Outline: User updates a project with a PUT request (Alternate Flow)
    Given a project with ID "<id>" and title "Project to Amend" exists
    When the user submits a PUT request to /projects/<id> with title "Amended Project" and description "New Description"
    Then the project API responds with status code 200
    And the response body confirms "title" as "Amended Project" and "description" as "New Description"
    And the system updates the project

    Examples:
      | id |
      | 2  |

  Scenario: User attempts to update a project with an invalid ID (Error Flow)
    When the user submits a PUT request to /projects/-1 with title "Invalid Update"
    Then the project API responds with status code 400
    And the response body contains "errorMessages" for "Invalid project ID"
    And the project is not stored in the system
