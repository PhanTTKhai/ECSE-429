Feature: Modify a Category
  As a user, I want to modify a category, so that I can update its name or description as needed.

  Background:
    Given the todo management API is running

  Scenario Outline: User modifies a category successfully (Normal Flow)
    When the user sends a PUT request to /categories/<category_id> with the new title "<new_title>" and new description "<new_description>"
    Then the API responds with status code 200 (OK)
    And the response body contains "title" of "<new_title>" and "description" of "<new_description>"
    And the system updates the category with ID "<category_id>"

    Examples:
      | category_id | new_title   | new_description        |
      | 1           | Work Tasks | Updated work tasks   |
      | 2           | Personal   | Updated personal info|
      | 3           | Fitness    | Updated fitness goals|
      | 4           | Shopping   | Updated shopping list|

  Scenario Outline: User attempts to modify a non-existent category (Error Flow)
    When the user sends a PUT request to /categories/<non_existent_id> with the new title "Updated Title"
    Then the API responds with status code 404 (Not Found)
    And the response body contains "errorMessages" 
    And no category is updated in the system

    Examples:
      | non_existent_id |
      | 99              |
      | 100             |

  Scenario Outline: User attempts to modify a category with missing or invalid fields (Alternative Flow)
    When the user sends a PUT request to /categories/<category_id> with an empty title "<empty_title>" and an empty description "<empty_description>"
    Then the API responds with status code 400 (Bad Request)
    And the response body contains "errorMessages" of "Failed Validation: title and description cannot be empty"
    And the category with ID "<category_id>" is not updated in the system

    Examples:
      | category_id | empty_title | empty_description |
      | 1           | ""         | ""                |
      | 2           | ""         | ""                |
