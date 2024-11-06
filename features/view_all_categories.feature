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

  Scenario: User sends an invalid request to view all categories
    Given the todo management API is running
    When the user sends an invalid GET request to /invalid/categories
    Then the API responds with status code 404 (Not Found)

