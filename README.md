# Unit Test Suite for Rest Api todo list manager

## Overview

This repository contains a suite of unit tests designed to validate the behavior of a REST API. The goal of this test
suite is to ensure that the API functions as expected.

## Structure

The test suite is divided into separate modules:

- todos
- categories
- projects
- interoperability

### Each module includes:

- Validation of Expected Behavior: Tests to confirm that the API performs as documented.
- Bug Identification: Tests that identify discrepancies between the documented behavior and the actual API behavior.
- Includes separate test cases for scenarios where the documented behavior fails and where the undocumented behavior
  allows the operation to succeed.
- Payload Format Tests: Tests that verify the API’s ability to handle JSON and XML payloads for input and output.

## Prerequisites

- Python 3.x installed on your system.
- Dependencies are installed. they can be installed with the following commands.<br>
  `pip install -r resources/requirements.txt`

## Running the Tests

The test suite can be run using the custom test runner class with command. This class will ensure that the API server is
started, all tests are executed, and the server is stopped afterward.<br>
`python run_api_tests.py`


 