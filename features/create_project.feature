Feature: Create a New Project
  As a user, I want to create a new project so that I can manage my tasks effectively.

  Background:
    Given the todo management API is running

  Scenario Outline: User creates a new project by specifying title and description (Normal Flow)
    When the user sends a POST request to /projects with title "<title>" and description "<description>"
    Then the API responds with status code 201 (Created)
    And the response body confirms "title" of "<title>" and "description" of "<description>"
    Then the system saves the project

    Examples:
      | title      | description         |
      | Project X  | Description X       |
      | Project Y  | Description Y       |
      | Project Z  | Description Z       |
    
  Scenario Outline: User creates a new project with empty title and description (Alternate Flow)
    When the user sends a POST request to /projects with empty title and description
    Then the API responds with status code 201 (Created)
    And the response body confirms "title" of "<title>" and "description" of "<description>"
    Then the system saves the project

  Scenario Outline: User attempts to create a project with an ID (Error Flow)
    When the user sends a POST request to /projects with an ID "<id>"
    Then the API responds with status code 400 (Bad Request)
    And the project is not stored in the system

    Examples:
      | id |
      | 101  |
      | 102  |
