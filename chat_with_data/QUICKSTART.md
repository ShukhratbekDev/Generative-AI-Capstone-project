# Quick Start Guide

## Get Started in 3 Steps

### Step 0: Navigate to Project Folder
```bash
cd chat_with_data
```

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Configure Environment
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### Step 3: Run the Application
```bash
streamlit run app.py
```

Or use the quick start script:
```bash
python run.py
```

## First Time Setup

The database will be automatically created on first run. If you want to manually initialize it:

```bash
python database.py
```

This creates `sales_data.db` with 600+ sales records.

## Testing the Application

1. **View Business Dashboard**: Check the sidebar for aggregated metrics and charts
2. **Try Sample Queries**: Click any sample query button in the sidebar
3. **Ask Custom Questions**: Type questions like:
   - "What are the top 5 products by sales?"
   - "Show me sales by region"
   - "Which customer spent the most?"
4. **Create Support Ticket**: Ask "Create a support ticket for [your issue]"

## Console Logging

All agent operations are logged to the console. Watch the terminal where you ran `streamlit run app.py` to see:
- User messages
- Function calls
- Database queries
- Support ticket creations
- Errors and warnings

## Troubleshooting

**Database not found?**
- The app auto-creates the database on first run
- Or run `python database.py` manually

**OpenAI API errors?**
- Check your `.env` file has `OPENAI_API_KEY` set
- Verify the API key is valid and has credits

**Support tickets not working?**
- They work in mock mode without GitHub credentials
- To enable real tickets, add GitHub credentials to `.env`

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [DEPLOYMENT.md](DEPLOYMENT.md) for deployment instructions
- Update [DEPLOYMENT_LINK.md](DEPLOYMENT_LINK.md) once deployed

