Feature: Update a Project
  As a user, I want to update details of a project to keep information current.

  Background:
    Given the todo management API is running

  Scenario Outline: User updates a project with a POST request (Normal Flow)
    Given a project with title <title> exists
    When the user sends a POST request to the corresponding /projects/id with a new title "Updated Project"
    Then the API responds with status code 200 (Ok)
    And the response body confirms "title" as "Updated Project"
    And the system updates the project

    Examples:
      | title |
      | "Project to Update" |

  Scenario Outline: User updates a project with a PUT request (Alternate Flow)
    Given a project with title <title> exists
    When the user sends a PUT request to the corresponding /projects/id with a new title "Amended Project"
    Then the API responds with status code 200 (Ok)
    And the response body confirms "title" as "Amended Project"
    And the system updates the project

    Examples:
        | title |
        | "Project to Update" |

  Scenario Outline: User attempts to update a project with an invalid ID (Error Flow)
    When the user sends a PUT request to /projects/<id> with a new title "Invalid Update"
    Then the API responds with status code 404 (Not Found)
    And the project is not stored in the system
    
    Examples:
      | id |
      | -1 |
