import os
import random
import subprocess

FEATURES_DIR = "features"
OUTPUT_FILE = "test_results.txt"  # Specify the output file for the results

def find_feature_files(directory):
    feature_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".feature"):
                feature_files.append(os.path.join(root, file))
    return feature_files

def run_feature_file(feature_file, output_file):
    print(f"Running feature: {feature_file}")
    
    # Run `behave` with the feature file
    result = subprocess.run(
        ["python3", "-m", "behave", feature_file],
        capture_output=True, text=True
    )
    
    # Write the standard output (which contains the detailed info you want) to a file
    with open(output_file, 'a') as f:
        f.write(f"Running feature: {feature_file}\n")
        f.write(result.stdout)
        f.write("\n\n")  # Add space between different feature file outputs

def run_tests_randomly():
    # Find all feature files
    feature_files = find_feature_files(FEATURES_DIR)
    # Shuffle the list to randomize the order
    random.shuffle(feature_files)

    # Run each feature file
    for feature_file in feature_files:
        run_feature_file(feature_file, OUTPUT_FILE)

if __name__ == "__main__":
    # Clear the output file before running tests (optional)
    with open(OUTPUT_FILE, 'w') as f:
        f.write("Test Run Results\n")
        f.write("="*20 + "\n\n")
    
    run_tests_randomly()
    print(f"Test results saved to {OUTPUT_FILE}")
