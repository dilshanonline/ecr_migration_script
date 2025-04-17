# This file contains the configuration for the source and target registries.

# SOURCE CONFIGURATION
PROJECT_ID = "my-project-id"  # Replace with your actual project ID
LOCATION = "europe"  # Replace with your actual location
SOURCE_REPO = "eu.gcr.io" # Replace with your actual source repository
IMAGE_PATH = "repo_name/old_image_name"  # Replace with your actual image path
SOURCE_FULL_REPO = f"europe-docker.pkg.dev/{PROJECT_ID}/{SOURCE_REPO}/{IMAGE_PATH}" # Replace with your actual full source repository

# TARGET CONFIGURATION
TARGET_REGISTRY = "0123456789.dkr.ecr.eu-west-1.amazonaws.com" # Replace with your actual target registry
TARGET_PATH = "new_image_name"  # Replace with your actual target image path
AWS_REGION = "eu-west-1" # Replace with your actual AWS region
DEFAULT_LIMIT = 2  # Default limit for the number of images to process
RETAGGED_LIST_FILE = "retagged_images.txt" # File to store the list of retagged images
LOG_DIR = "logs" # Directory to store logs
SSO_PROFILE = "aws-sso-profile"  # Replace with your actual AWS SSO profile name