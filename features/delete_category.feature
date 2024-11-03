Feature: Delete a Category
  As a user, I want to delete a category, so that I can remove categories that I no longer need.

  Background:
    Given the todo management API is running

  Scenario Outline: User deletes a category successfully (Normal Flow)
    When the user sends a DELETE request to /categories/<category_id>
    Then the API responds with status code 200 (OK)
    And the system no longer contains the category with ID "<category_id>"

    Examples:
      | category_id |
      | 1           |
      | 2           |
      | 3           |
      | 4           |

  Scenario Outline: Scenario Outline name: User attempts to delete a non-existent category (Error Flow)
    When the user sends a DELETE request to /categories/<non_existent_id>
    Then the API responds with status code 404 (Not Found)
    And the response body contains "errorMessages" of "Category not found"
    And the system does not contain a category with ID "<non_existent_id>"

    Examples:
      | non_existent_id |
      | 99              |
      | 100             |

  Scenario Outline: User attempts to delete a category that has todos (Alternative Flow)
    Given there are todos associated with category "<category_with_todos>"
    When the user sends a DELETE request to /categories/<category_with_todos>
    Then the API responds with status code 200 (OK)
    And the todos associated with category "<category_with_todos>" are no longer linked to any category

    Examples:
      | category_with_todos |
      | 5                   |
      | 6                   |