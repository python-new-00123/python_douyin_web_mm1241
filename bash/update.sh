#!/bin/bash

# Ask for confirmation to proceed with the update
read -r -p "Do you want to update python_douyin_web_mm1241? [y/n] " input
case $input in
    [yY])
        # Navigate to the project directory or exit if it fails
        cd /www/wwwroot/python_douyin_web_mm1241 || { echo "The directory does not exist."; exit 1; }

        # Pull the latest changes from the repository
        git pull

        # Activate the virtual environment
        source venv/bin/activate

        # Optionally, update Python dependencies
        pip install -r requirements.txt

        # Deactivate the virtual environment
        deactivate

        # Restart the service to apply changes
        echo "Restarting python_douyin_web_mm1241 service"
        sudo systemctl restart python_douyin_web_mm1241.service
        echo "Successfully restarted all services!"
        ;;
    [nN]|*)
        echo "Exiting..."
        exit 1
        ;;
esac
