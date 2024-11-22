Feature: View a Project
  As a user, I want to view specific details of a project.

  Background:
    Given the todo management API is running
    And the initial project list is captured


  Scenario Outline: User retrieves a project by ID (Normal Flow)
    Given a project with title <title> exists
    When the user sends a GET request to with the corresponding projects id
    Then the API responds with status code 200 (OK)
    And the response body confirms the correct id and corresponding title

    Examples:
      | title              |
      | "Project to Get" |

  Scenario Outline: User retrieves a project by accessing an associated tasks (Alternate Flow)
    Given a project with title "<title>" exists
    And tasks are associated with the project
    When the user sends a GET request to retrieve the project through the tasks' project association
    Then the API responds with status code 200 (OK)
    And the response body confirms the correct id and corresponding title

    Examples:
      | title            |
      | "Project with Todo" |

  Scenario Outline: User attempts to retrieve a project with an invalid ID (Error Flow)
    When the user sends a GET request with id "<id>"
    Then the API responds with status code 404 (Not Found)
    Then the system does not create or modify any projects

    Examples:
      | id  |
      | -1  |
