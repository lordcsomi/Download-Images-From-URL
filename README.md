# Image Downloader Installation Guide

This script allows you to download images from a specific URL template and validates that the downloaded images are not corrupt. Before running the script, you need to set up the environment and install the necessary dependencies.

 Prerequisites

 - Python 3.x installed (https://www.python.org/downloads/)
 - pip package manager installed (usually comes with Python)

# Installation Steps

 1. Clone or download the script from the repository.
 2. Open a terminal or command prompt.
 3. Navigate to the directory where you have the script.
 4. Create a virtual environment **optional**:
    ```bash
    python -m venv venv
    ```
     Activate the virtual environment:
      - On Windows:
        ```bash
        venv\Scripts\activate
        ```
      - On macOS and Linux:
        ```bash
        source venv/bin/activate
        ```
 5. Install the required Python packages using pip:
    ```bash
    pip install aiohttp pillow
    ```
 6. Customize the script:
    - Set the `URL` variable to your specific image URL template. In the `URL` place a `{}` where you want the loop
    - Modify the `DOWNLOADE_PATH` variable to specify the download path.
    - Modify the `TRASHOLD` to set a tarshold
    - Modify the `START` to set the starting number of the loop
    - Modify the `END` to set the ending number of the loop
# Run the script:  
  ```
  python main.py
  ```
  The script will download images to the specified download path and validate their integrity. It will print messages indicating the download status.

# Made by Csomi
That's it! You have successfully installed and run the image downloader script. Enjoy downloading your images!
