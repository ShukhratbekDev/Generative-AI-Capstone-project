# Deployment Information

## Hosted Solution Link

**Note**: This document should be updated with the actual deployment link once the application is deployed to Hugging Face Spaces or another hosting platform.

### Hugging Face Spaces

Once deployed, the application will be available at:
```
https://huggingface.co/spaces/Shukhratbek/data-insights-app
```

### Deployment Steps Completed

✅ Project structure created
✅ Database schema and data generation (600+ rows)
✅ AI Agent with function calling (2 tools: query_database, create_support_ticket)
✅ Safety features implemented (blocks dangerous SQL operations)
✅ Streamlit UI with business dashboard
✅ Console logging implemented
✅ Support ticket integration (GitHub Issues)
✅ README with instructions

### To Deploy:

1. Create a Hugging Face Space (Streamlit SDK)
2. Upload all project files
3. Set environment variables in Space settings:
   - OPENAI_API_KEY
   - GITHUB_TOKEN (optional)
   - GITHUB_REPO_OWNER (optional)
   - GITHUB_REPO_NAME (optional)
4. The Space will auto-deploy

### Local Testing

Before deploying, test locally:
```bash
# Install dependencies
pip install -r requirements.txt

# Initialize database
python database.py

# Run application
streamlit run app.py
```

### Update This Document

Once deployed, replace the placeholder URL above with the actual Hugging Face Spaces link.

---

**Project**: Data Insights App - Capstone Project 1
**Status**: Ready for deployment
**Last Updated**: [Date when deployed]

