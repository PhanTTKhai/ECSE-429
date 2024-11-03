Feature: View All Todos of a Category
  As a user, I want to view all todos under a specific category, so that I can see tasks grouped by category.

  Background:
    Given the todo management API is running

  Scenario Outline: User views all todos of a specific category successfully (Normal Flow)
    When the user sends a GET request to /categories/<category_id>/todos
    Then the API responds with status code 200 (OK)
    And the response body contains a list of all todos associated with the category ID "<category_id>"


  Scenario Outline: User views todos of a non-existent category (Error Flow)
    When the user sends a GET request to /categories/<non_existent_id>/todos
    Then the API responds with status code 404 (Not Found)
    And the response body contains "errorMessages" of "Category not found"
    And no todos are returned

    Examples:
      | non_existent_id |
      | 99              |
      | 100             |

  Scenario Outline: User views todos of a category with no todos (Alternative Flow)
    Given the category with ID "<category_id>" has no associated todos
    When the user sends a GET request to /categories/<category_id>/todos
    Then the API responds with status code 200 (OK)
    And the response body contains an empty list

    Examples:
      | category_id |
      | 5           |
      | 6           |
