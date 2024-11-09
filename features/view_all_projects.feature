Feature: Retrieve all Projects
  As a user, I want to retrieve details of specific projects to view their information.

  Background:
    Given the todo management API is running

  Scenario Outline: User retrieves all existings projects (Normal Flow)
    Given at least <no> project exists 
    And the initial project list is captured
    When the user sends a GET request on /projects
    Then the API responds with status code 200 (OK)
    And the response body contains all projects
  
    Examples:
      | no |
      | 1 |
      | 2 |
      | 3 |

  Scenario Outline: User retrieves all projects by iterating through project IDs (Alternate Flow)
    Given at least <no> project exists
    And the initial project list is captured
    When the user sends a GET request to retrieve each project by its ID
    Then the API responds with status code 200 (OK) for each project
    And each response body confirms the correct project ID and title

    Examples:
      | no |
      | 1 |
      | 2 |
      | 3 |


  Scenario: User attempts to retrieve all projects by leaving empty id (Error Flow)
    When the user submits a GET request to /projects/
    Then the API responds with status code 404 (Not Found)
