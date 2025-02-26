# GitLab CI/CD Setup Guide

## 1. Create GitLab Group and Project

1. **Create a Group:**
   - Log into GitLab
   - Click on "Groups" → "Create group"
   - Fill in group details and click "Create group"

2. **Create a Project:**
   - In your group, click "New project"
   - Choose "Create blank project"
   - Fill in project name and settings
   - Click "Create project"

3. **Push Required Files:**
    - Open a terminal and navigate to your project directory
    - Initialize a new Git repository:
      ```sh
      git init
      ```
    - Add all files to the repository:
      ```sh
      git add .
      ```
    - Commit the files:
      ```sh
      git commit -m "Initial commit with required project files"
      ```
    - Add the remote repository URL:
      ```sh
      git remote add origin <your-repository-url>
      ```
    - Push the files to the remote repository:
      ```sh
      git push -u origin master
      ```


## 2. Required Project Files

You will need to create the following files in your project:

1. **app.py:**
   - Main Python application file
   - Should contain a simple Flask web application
   - Must listen on host '0.0.0.0' and port 5000

2. **Dockerfile:**
   - Use Python base image
   - Set up working directory
   - Install dependencies
   - Copy application files
   - Configure container startup

3. **requirements.txt:**
   - List all Python dependencies
   - Must include Flask

4. **.gitlab-ci.yml:**
   - Define CI/CD pipeline stages
   - Configure Docker-in-Docker service
   - Include build and test stages
   - Specify Docker build commands

## 3. Running Pipeline

Note: Detailed implementation of app.py, Dockerfile, and .gitlab-ci.yml will be added separately.
