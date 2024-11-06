Feature: Update Category Details
  As a user, I want to edit the details of a category so that I can keep my categories accurate and reflective of current information.

  Background:
    Given the todo management API is running

  Scenario Outline: The user successfully updates a category's details using PUT method.
    Given there are categories stored in the system
      | title       | description         |
      | <title>     | <description>       |
    When the user updates the "<field>" of category "<title>" to "<value>" with PUT
    Then the API responds with status code 200 (OK)

    Examples:
      | title       | description           | field       | value                   |
      | Work Tasks  | Initial work tasks    | title       | Updated Work Tasks      |
      | Personal    | Personal information  | title       | Updated personal info   |
      | Fitness     | Goals for fitness     | title       | Updated Fitness Goals   |

  Scenario Outline: The user successfully updates a category's details using POST method.
    Given there are categories stored in the system
      | title       | description         |
      | <title>     | <description>       |
    When the user updates the "<field>" of category "<title>" to "<value>" with POST
    Then the API responds with status code 200 (OK)

    Examples:
      | title       | description           | field       | value                   |
      | Work Tasks  | Initial work tasks    | title       | Updated Work Tasks      |
      | Personal    | Personal information  | description | Updated personal info   |
      | Fitness     | Goals for fitness     | title       | Updated Fitness Goals   |

  Scenario Outline: User attempts to update a non-existent category.
    Given there is no category with ID "<category_id>"
    When the user tries to update the category with ID "<category_id>" 
    Then the API responds with status code 404 (Not Found)
    And the system does not create or modify any categories

    Examples:
      | category_id |
      | 0           |
      | -1          |
      | 999         |
      | 12345       |
