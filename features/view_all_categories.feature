Feature: View All Categories
  As a user, I want to view all categories, so that I can see the organization of my todos and projects.

  Background:
    Given the todo management API is running

  Scenario: User views all categories successfully (Normal Flow)
    When the user sends a GET request to /categories
    Then the API responds with status code 200 (OK)
    And the response body contains a list of all categories

  Scenario: User views all categories but no categories exist (Alternative Flow)
    Given there are no categories in the system
    When the user sends a GET request to /categories
    Then the API responds with status code 200 (OK)
    And the response body contains an empty list

  Scenario: API error when viewing categories (Error Flow)
    Given the API is experiencing an issue
    When the user sends a GET request to /categories
    Then the API responds with status code 500 (Internal Server Error)
    And the response body contains "errorMessages" of "Internal Server Error"
