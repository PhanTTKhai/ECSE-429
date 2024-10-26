Feature: Create a new project

    As a user, I would like to add a new project to the system so that I can track the project's progress.
    Background:
        Given the todo management API is running

    # Normal flow
    Scenario Outline: POST a new project with all fields
        When the user sends a POST request to /projects with the title <title>, completed <completed>, active <active>, and description <description>
        Then the project <title> should appear in the system
        Examples:
            | title  | completed  | active    | description   |
            | P1     | False      | False     | Project 1     |
            | P2     | True       | True      | Project 2     |

    # Alternate flow
    Scenario Outline: POST a new project with only required fields
        When the user sends a POST request to /projects with the title <title>
        Then the project <title> should appear in the system
        Examples:
            | title  |
            | P3     |
            | P4     |

    # Error flow
    Scenario Outline: POST a new project with only an id
        When the user sends a POST request to /projects with the id <id>
        Then the system should respond with an error status code
        Examples:
            | id  |
            | 10  |
            | 11  |