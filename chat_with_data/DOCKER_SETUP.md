# Docker Setup for Hugging Face Spaces

## Quick Reference

This project is configured for deployment to Hugging Face Spaces using Docker.

## Files Required

- ✅ `Dockerfile` - Docker configuration
- ✅ `.dockerignore` - Files to exclude from Docker build
- ✅ `requirements.txt` - Python dependencies
- ✅ `app.py` - Main Streamlit application

## Dockerfile Overview

The Dockerfile:
- Uses Python 3.11 slim base image
- Installs system dependencies (gcc for compiling Python packages)
- Installs Python dependencies from requirements.txt
- Copies all application files
- Exposes port 8501 (Streamlit default)
- Runs Streamlit on container startup

## Deployment Steps

1. **Create Hugging Face Space**
   - Go to https://huggingface.co/spaces
   - Select "Docker" as the SDK
   - Create the space

2. **Upload Files**
   - Upload all files from the `chat_with_data/` folder
   - Make sure `Dockerfile` is in the root of the Space repository

3. **Set Environment Variables**
   - In Space settings → "Variables and secrets"
   - Add:
     - `OPENAI_API_KEY`
     - `GITHUB_TOKEN` (optional)
     - `GITHUB_REPO_OWNER` (optional)
     - `GITHUB_REPO_NAME` (optional)

4. **Deploy**
   - Push files to the Space
   - Hugging Face will automatically build the Docker image
   - Wait 5-10 minutes for build to complete

## Local Docker Testing

To test the Docker setup locally:

```bash
# Build the image
docker build -t data-insights-app .

# Run the container
docker run -p 8501:8501 \
  -e OPENAI_API_KEY=your_key_here \
  data-insights-app
```

Then visit http://localhost:8501

## Troubleshooting

**Build fails:**
- Check that all files are present
- Verify requirements.txt has no syntax errors
- Check Docker logs in Hugging Face Spaces

**App doesn't start:**
- Verify port 8501 is exposed
- Check environment variables are set correctly
- Review application logs in Space

**Database issues:**
- The app auto-creates the database on first run
- Database is ephemeral (resets on redeploy)

## Notes

- The database (`sales_data.db`) is created automatically on first app startup
- Environment variables are read from Hugging Face Space secrets
- All console logs are visible in the Space's logs section

