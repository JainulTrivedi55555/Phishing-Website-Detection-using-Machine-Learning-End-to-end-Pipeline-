# This file is used to store application-wide constants.
# You can add global variables here that are used across different modules.

# For example, you could define paths here, although ROOT_DIR is already handled in app.py.
import os


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define any other constants your application needs.
# e.g.,
BUCKET_NAME = "my-ml-bucket"
MODEL_FILENAME = "trained_model.pkl"

