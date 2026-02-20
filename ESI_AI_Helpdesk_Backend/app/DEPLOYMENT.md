# Deployment Guide: Deploying Backend on Render

Render url for backend web server: https://ai-helpdesk-system-vas2.onrender.com
Swagger doc: https://ai-helpdesk-system-vas2.onrender.com/docs

## Prerequisites
Before deploying the backend application on Render, ensure the following:

1. **GitHub Repository**:
   - Your backend code is published on a GitHub repository.
   - Ensure the repository is public or you have provided Render access to your private repository.

2. **Render Account**:
   - Create an account on [Render](https://render.com/).

3. **Environment Variables**:
   - Prepare a `.env` file with all necessary environment variables (e.g., database credentials, secret keys).

4. **Dependencies**:
   - Ensure all dependencies are listed in `requirements.txt`.

5. **Procfile** (Optional):
   - If your application requires specific commands to run, create a `Procfile` with the command (e.g., `web: uvicorn app.main:app --host 0.0.0.0 --port 8000`).

## Deployment Flow

### Step 1: Publish Code to GitHub
1. Initialize a Git repository in your project folder (if not already done):
   ```bash
   git init
   ```
2. Add all files to the repository:
   ```bash
   git add .
   ```
3. Commit the changes:
   ```bash
   git commit -m "Initial commit"
   ```
4. Push the code to GitHub:
   ```bash
   git remote add origin <your-repo-url>
   git branch -M main
   git push -u origin main
   ```

### Step 2: Connect Repository to Render
1. Log in to your Render account.
2. Click on **New +** and select **Web Service**.
3. Connect your GitHub account and select the repository containing your backend code.

### Step 3: Configure the Service
1. **Environment**:
   - Choose the environment (e.g., Python).
2. **Build Command**:
   - Use the following command to install dependencies:
     ```bash
     pip install -r requirements.txt
     ```
3. **Start Command**:
   - Specify the command to start the application, e.g.:
     ```bash
     uvicorn app.main:app --host 0.0.0.0 --port 8000
     ```
4. **Environment Variables**:
   - Add all required environment variables from your `.env` file in the Render dashboard.

### Step 4: Deploy
1. Click **Create Web Service**.
2. Render will automatically build and deploy your application.
3. Once deployed, you will receive a URL to access your backend.

## Post-Deployment
- Test the deployed application using the provided URL.
- Monitor logs in the Render dashboard for any issues.
- Update the repository and redeploy as needed (Render will automatically detect changes and trigger a new deployment).