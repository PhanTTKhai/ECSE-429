Feature: Delete a Project
  As a user, I want to delete projects that are no longer needed.

  Background:
    Given the todo management API is running
    And the initial project list is captured

  Scenario Outline: User deletes an existing project by ID (Normal Flow)
    Given a project with title <title> exists
    When the user sends a DELETE request using the corresponding projects id
    Then the API responds with status code 200 (OK)
    And the system removes the project from the database

    Examples:
      | title              |
      | "Project to Delete" |

  Scenario Outline: User attempts to delete a project with associated todos (Alternate Flow)
    Given a project with title <title> exists
    And todos are associated with the project
    When the user sends a DELETE request using the corresponding projects id
    Then the API responds with status code 200 (OK)
    And the system removes the project and its associated todos from the database

    Examples:
      | title                |
      | "Project with Todos" |

  Scenario Outline: User attempts to delete a project with an invalid ID (Error Flow)
    Given there is no project with id "<project_id>"
    When the user sends a DELETE request with id "<project_id>"
    Then the API responds with status code 404 (Not Found)
    And the system does not create or modify any projects

    Examples:
      | project_id |
      | -1         |
