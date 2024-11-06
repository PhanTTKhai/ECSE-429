Feature: Delete a Category

  Scenario Outline: User deletes a category successfully (Normal Flow)
    Given a category exists with title "<title>"
    When the user sends a DELETE request to delete the category
    Then the category API responds with status code 200
    And the category with title "<title>" is no longer in the system

    Examples:
      | title      |
      | Work       |
      | Personal   |
      | Shopping   |
      | Exercise   |

  Scenario Outline: User attempts to delete a non-existent category (Error Flow)
    When the user sends a DELETE request to delete a category with ID "<invalid_id>"
    Then the category API responds with status code 404
    And the response body contains "errorMessages"
    And no changes are made to the system

    Examples:
      | invalid_id |
      | 999       |
      | -1        |
      | abc       |
      | 0         |

  Scenario Outline: User deletes a category that has associated items (Alternative Flow)
    Given a category with title "{title}" and description "{description}" exists for deletion
    And there are items associated with this category
    When the user sends a DELETE request to delete the category
    Then the category API responds with status code 200
    And the category with title "<title>" is no longer in the system
    And the associated items no longer reference the deleted category

    Examples:
      | title      | description         |
      | Work       | Tasks for work      |
      | Personal   | Personal activities |
      | Shopping   | Groceries and items |
      | Exercise   | Exercise routines   |