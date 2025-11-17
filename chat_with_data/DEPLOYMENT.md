# Deployment Guide - Data Insights App

## Hugging Face Spaces Deployment

This guide explains how to deploy the Data Insights App to Hugging Face Spaces.

### Prerequisites

1. Hugging Face account (sign up at https://huggingface.co)
2. OpenAI API key
3. (Optional) GitHub token for support tickets

### Step-by-Step Deployment

#### 1. Create a New Space

1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. Fill in the details:
   - **Space name**: `data-insights-app` (or your preferred name)
   - **SDK**: Select "Streamlit"
   - **Visibility**: Public or Private (your choice)
4. Click "Create Space"

#### 2. Upload Files

Upload the following files to your Space repository:

- `app.py` (main application file)
- `agent.py` (AI agent with function calling)
- `database.py` (database utilities)
- `github_ticket.py` (support ticket integration)
- `requirements.txt` (dependencies)
- `README.md` (documentation)

#### 3. Configure Environment Variables

1. In your Space settings, go to "Variables and secrets"
2. Add the following secrets:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `GITHUB_TOKEN`: (Optional) Your GitHub personal access token
   - `GITHUB_REPO_OWNER`: (Optional) Your GitHub username
   - `GITHUB_REPO_NAME`: (Optional) Repository name for support tickets

#### 4. Initialize Database

Since Hugging Face Spaces doesn't persist files between restarts, you'll need to modify the app to initialize the database on startup. The current `app.py` already handles this, but you may want to add a check.

Alternatively, you can:
- Pre-create the database and upload it
- Or modify the code to auto-initialize if the database doesn't exist

#### 5. Deploy

1. Push your files to the Space repository
2. Hugging Face will automatically build and deploy your app
3. Wait for the build to complete (usually 2-5 minutes)
4. Your app will be live at: `https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME`

### Post-Deployment

1. Test the application by asking sample questions
2. Verify that the database initializes correctly
3. Test support ticket creation (if GitHub credentials are configured)
4. Check console logs in the Space logs section

### Example Space URL

Once deployed, your Space URL will look like:
```
https://huggingface.co/spaces/yourusername/data-insights-app
```

### Troubleshooting

**Database not persisting**: 
- Hugging Face Spaces reset on each deployment
- Consider using a persistent storage solution or initialize on each startup

**API Key errors**:
- Verify secrets are correctly set in Space settings
- Check that variable names match exactly (case-sensitive)

**Build failures**:
- Check the logs in the Space's "Logs" tab
- Verify all dependencies are in `requirements.txt`
- Ensure Python version compatibility

### Alternative Deployment Options

#### Streamlit Cloud

1. Push code to GitHub
2. Go to https://share.streamlit.io
3. Connect your GitHub repository
4. Configure environment variables
5. Deploy

#### Local Deployment

For local testing:
```bash
python database.py  # Initialize database
streamlit run app.py
```

### Support

For deployment issues, create a support ticket using the in-app feature or contact the development team.

