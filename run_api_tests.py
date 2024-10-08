import unittest
import random
import requests
import subprocess
import time

# Import all test modules
from test_api_todos import TestAPITodos
from test_api_projects import TestAPIProjects

SERVER_URL = "http://localhost:4567"


def start_server():
    try:
        response = requests.get(SERVER_URL)
        if response.status_code == 200:
            print("Server is already running.")
            return None
    except requests.exceptions.ConnectionError:
        print("Starting the server...")
        process = subprocess.Popen(['java', '-jar', 'resources/runTodoManagerRestAPI-1.5.5.jar'])
        time.sleep(5)
        return process


def stop_server(process):
    if process:
        process.terminate()
        print("Server terminated.")


def suite():
    test_suite = unittest.TestSuite()

    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestAPITodos))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestAPIProjects))

    test_list = list(test_suite)
    random.shuffle(test_list)
    shuffled_suite = unittest.TestSuite(test_list)

    return shuffled_suite


if __name__ == '__main__':
    server_process = start_server()
    try:
        runner = unittest.TextTestRunner()
        runner.run(suite())
    finally:
        stop_server(server_process)
