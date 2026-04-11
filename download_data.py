import os
import kaggle

# Tell Kaggle exactly where to find the config file we just created
os.environ['KAGGLE_CONFIG_DIR'] = os.path.expanduser('~/.kaggle')

# Define the target path
download_path = r'D:\samruddhi\ai_project\backend\model\dataset'

if not os.path.exists(download_path):
    os.makedirs(download_path)

print("--- Step 1: Connecting to Kaggle ---")
api = kaggle.KaggleApi()
api.authenticate()

print(f"--- Step 2: Downloading to {download_path} ---")
# This will download the zip file
api.competition_download_files('state-farm-distracted-driver-detection', path=download_path)

print("--- Step 3: Download Complete! ---")