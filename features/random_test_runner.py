import os
import random
import subprocess

FEATURES_DIR = "features"

def find_feature_files(directory):
    feature_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".feature"):
                feature_files.append(os.path.join(root, file))
    return feature_files

def run_feature_file(feature_file):
    print(f"Running feature: {feature_file}")
    
    # Run `behave` with the feature file
    result = subprocess.run(
        ["python3", "-m", "behave", feature_file],
        capture_output=True, text=True
    )
    
    # Print the standard output (which contains the detailed info you want)
    print(result.stdout)

def run_tests_randomly():
    # Find all feature files
    feature_files = find_feature_files(FEATURES_DIR)
    # Shuffle the list to randomize the order
    random.shuffle(feature_files)

    # Run each feature file
    for feature_file in feature_files:
        run_feature_file(feature_file)

if __name__ == "__main__":
    run_tests_randomly()
