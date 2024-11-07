Feature: Create a New Category
    As a user, I want to create a new category so that I can keep track of my todos and projects effectively
  Background:
    Given the todo management API is running

  Scenario Outline: User creates a new category successfully (Normal Flow)
    When the user submits a POST request to create a category with the title "<title>"
    Then the category API responds with status code 201
    And the response body confirms "title" as "<title>"
    Then the system stores the new category

    Examples:
      | title      |
      | Work       |
      | Personal   |
      | Shopping   |
      | Exercise   |

  Scenario Outline: User creates a new category with description (Alternative Flow)
    When the user submits a POST request to create a category with the title "<title>" and description "<description>"
    Then the category API responds with status code 201
    And the response body confirms "title" as "<title>"
    And the response body includes "description" as "<description>"
    Then the system stores the new category

    Examples:
      | title      | description         |
      | Work       | Tasks for work      |
      | Personal   | Personal activities |
      | Shopping   | Groceries and items |
      | Exercise   | Exercise routines   |

  Scenario: User attempts to create a category with an ID (Error Flow)
    When the user submits a POST request to create a category with an ID 
    Then the category API responds with status code 400
    And the response body contains "errorMessages" 
    And the category is not stored in the system
