# Deployment Guide - Voice to Image App

## Hugging Face Spaces Deployment

This guide explains how to deploy the Voice to Image App to Hugging Face Spaces.

### Prerequisites

1. Hugging Face account (sign up at https://huggingface.co)
2. OpenAI API key

### Step-by-Step Deployment

#### 1. Create a New Space

1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. Fill in the details:
   - **Space name**: `voice-to-image-app` (or your preferred name)
   - **SDK**: Select **"Docker"**
   - **Visibility**: Public or Private (your choice)
4. Click "Create Space"

#### 2. Upload Files

Upload the following files to your Space repository:

- `Dockerfile` (Docker configuration - **required**)
- `app.py` (main application file)
- `agent.py` (AI agent)
- `audio_processor.py` (audio processing)
- `requirements.txt` (dependencies)
- `.streamlit/config.toml` (Streamlit configuration - **important for file uploads**)
- `.dockerignore` (optional, but recommended)
- `README.md` (documentation)

**Important**: The `.streamlit/config.toml` file disables XSRF protection, which is necessary for file uploads to work on Hugging Face Spaces.

#### 3. Configure Environment Variables

1. In your Space settings, go to "Variables and secrets"
2. Add the following secret:
   - `OPENAI_API_KEY`: Your OpenAI API key

#### 4. Deploy

1. Push your files to the Space repository (including the `Dockerfile`)
2. Hugging Face will automatically detect the Dockerfile and build the Docker image
3. Wait for the build to complete (usually 5-10 minutes for Docker builds)
4. Your app will be live at: `https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME`

**Note**: Docker builds take longer than SDK builds but offer more control and flexibility.

### Post-Deployment

1. Test the application using the **text input feature** (most reliable on Hugging Face Spaces)
2. Try file upload if needed (may encounter 403 errors due to Spaces restrictions)
3. Test microphone recording (may not work due to network/proxy issues)
4. Verify image generation works correctly
5. Check console logs in the Space logs section

**Note**: Due to Hugging Face Spaces limitations:
- **Text input is the most reliable method** for generating images
- File uploads may be blocked (403 errors)
- Microphone recording may not work

### Troubleshooting

**Build failures**:
- Check the logs in the Space's "Logs" tab
- Verify all dependencies are in `requirements.txt`
- Ensure Python version compatibility
- For Docker: Verify the Dockerfile is correct and all files are present
- Check that the Dockerfile exposes port 8501 (Streamlit default)

**Audio recording issues**:
- Hugging Face Spaces may have limitations with microphone access
- Browser recording may not work due to network/proxy configuration
- **File uploads may fail with 403 errors** due to Hugging Face Spaces security restrictions
- **Recommended workaround**: Use the text input feature in the app to type descriptions directly
- Check browser permissions if attempting to use microphone

**API errors**:
- Verify secrets are correctly set in Space settings
- Check that variable names match exactly (case-sensitive)
- Ensure your OpenAI API key has access to DALL-E 3

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
pip install -r requirements.txt
streamlit run app.py
```

### Support

For deployment issues, create an issue in the repository or contact support.


