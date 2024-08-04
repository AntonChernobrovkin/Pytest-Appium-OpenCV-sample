Sample Pytest+Appium project with OpenCV.
Tuned for case when we cannot access buttons with Selenium
and have to find them with image search by OpenCV

## Pre-requisites
- Host with Appium
- Fresh Python (3.12 used while development)
- Python modules installed with `$pip install -r requirements.txt`

## Usage
- Set device capabilities and Appium url in dynamic_env.py 
- Connect device to host, start Appium
- Start test with `$pytest` from root directory of project