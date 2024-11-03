Feature: Create a New Category
  As a user, I want to create a new category, so that I can organize my todos and projects effectively.

  Background:
    Given the todo management API is running

  Scenario Outline: User creates a new category successfully (Normal Flow)
    When the user sends a POST request to /categories with the title "<title>"
    Then the API responds with status code 201 (Created)
    And the response body contains "title" of "<title>"
    Then the system saves the category

    Examples:
      | title      |
      | Work       |
      | Personal   |
      | Shopping   |
      | Exercise   |

  Scenario Outline: User creates a new category with description (Alternative Flow)
    When the user sends a POST request to /categories with the title "<title>" and description "<description>"
    Then the API responds with status code 201 (Created)
    And the response body contains "title" of "<title>"
    Then the system saves the category

    Examples:
      | title       | description           |
      | Work       | "Tasks for work"      |
      | Personal   | "Personal activities" |
      | Shopping   | "Groceries and items" |
      | Exercise   | "Exercise routines"   |

  Scenario: User attempts to create a category with an ID (Error Flow)
    When the user sends a POST request to /categories with an ID 
    Then the API responds with status code 400 (Bad Request)
    And the response body contains "errorMessages" 
    And the category is not stored in the system
