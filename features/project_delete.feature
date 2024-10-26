Feature: Delete a project

    As a user, I would like to delete a specific project from the system to indicate that the project is completed. 
    
    # Normal flow
    Scenario Outline: DELETE a project with a specific id
        Given the system is running and a project with title <title> exists
        When the user deletes the project with title <title>
        Then the project with title <title> should be deleted from the system
        Examples:
            | title  |
            | P10   |
            | P12   |

    # Alternate flow
    Scenario Outline: Mark a project as completed
        Given the system is running and a project with title <title> exists
        When the user updates the project with title <title> as with field completed <completed>
        Then the project with title <title> should be marked as completed
        Examples:
            | title            | completed |
            | testing update 1 | true      |
            | updated          | true      |

    # Error flow
    Scenario Outline: DELETE a project with an id that doesn't exist
        Given the system is running and there is no project with id <id>
        When the user sends a DELETE request to /projects/<id>
        Then the system should respond with an error status code and no project should be deleted
        Examples:
            | id             |
            | 9999999        |
            | 5318708217489  |