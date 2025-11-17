# Data Insights App - Project Summary

## Capstone Project 1: Chat with Data

### Project Overview

This project implements a **Data Insights Application** that allows users to interact with a sales database using natural language queries through an AI agent. The agent uses OpenAI's function calling API to safely query the database and create support tickets when needed.

### ✅ Requirements Met

#### Functional Requirements

- ✅ **AI Agent with Database Access**: Agent assists users in getting information from the database
- ✅ **Safe Data Handling**: Only extracted chunks/query results pass through to LLM, not the full database
- ✅ **Business Information UI**: Sidebar displays aggregated information (row counts, charts, tables, sample queries)
- ✅ **Console Logging**: All agent operations are logged to console with timestamps
- ✅ **Support Ticket Creation**: Agent can create GitHub issues for human assistance (explicitly or when suggested)
- ✅ **Function Calling**: Uses OpenAI's function calling API with 2+ tools

#### Non-Functional Requirements

- ✅ **Code in Root Branch**: All code is in the main branch
- ✅ **500+ Rows of Data**: Database contains 600 sales records
- ✅ **Python Implementation**: Entire project built with Python
- ✅ **Streamlit UI**: User interface built with Streamlit
- ✅ **Multiple Tools**: 2 function calling tools (query_database, create_support_ticket)
- ✅ **README with Instructions**: Comprehensive README with setup and usage instructions
- ✅ **Safety Features**: Blocks dangerous operations (DELETE, DROP, UPDATE, etc.)
- ✅ **Deployment Ready**: Includes deployment guide for Hugging Face Spaces

### Project Structure

```
Generative-AI-Capstone-project/
├── app.py                 # Main Streamlit application
├── agent.py               # AI agent with function calling
├── database.py            # Database setup and utilities
├── github_ticket.py       # Support ticket integration
├── requirements.txt       # Python dependencies
├── run.py                 # Quick start script
├── README.md              # Project documentation
├── DEPLOYMENT.md          # Deployment guide
├── DEPLOYMENT_LINK.md     # Deployment link document
├── PROJECT_SUMMARY.md     # This file
└── .env.example           # Environment variables template
```

### Key Features

1. **Safe Database Queries**
   - Only SELECT queries allowed
   - Blocks dangerous SQL keywords
   - Error handling and validation

2. **AI Agent Capabilities**
   - Natural language understanding
   - Automatic query generation
   - Intelligent response formatting
   - Context-aware suggestions

3. **Business Dashboard**
   - Total sales records count
   - Revenue metrics
   - Top products visualization
   - Regional sales distribution
   - Category breakdown
   - Sales trends over time

4. **Support Ticket System**
   - GitHub Issues integration
   - Automatic ticket creation
   - User-friendly error handling
   - Mock mode when credentials not configured

5. **User Experience**
   - Sample queries sidebar
   - Interactive charts (Plotly)
   - Real-time chat interface
   - Reset conversation option

### Technology Stack

- **Python 3.8+**: Core language
- **Streamlit**: Web UI framework
- **OpenAI API**: GPT-4 with function calling
- **SQLite**: Database
- **Pandas**: Data manipulation
- **Plotly**: Interactive visualizations
- **PyGithub**: GitHub API integration

### Database Schema

**sales table** (600+ records):
- Transaction details (date, customer, product, category)
- Financial data (quantity, unit_price, total_amount)
- Geographic data (region)
- Sales representative information

**customers table**:
- Customer information
- Aggregated statistics (total_orders, total_spent)

### Safety Features

The application includes multiple layers of safety:

1. **Query Validation**: Only SELECT statements allowed
2. **Keyword Blocking**: Prevents DROP, DELETE, UPDATE, INSERT, etc.
3. **Error Handling**: Graceful error messages
4. **Logging**: All operations logged for audit

### Function Calling Tools

1. **query_database**
   - Executes safe SELECT queries
   - Returns structured results
   - Handles errors gracefully

2. **create_support_ticket**
   - Creates GitHub issues
   - Supports labels and descriptions
   - Returns issue URL

### Console Logging

All operations are logged with:
- Timestamps
- Log levels (INFO, WARNING, ERROR)
- Function calls
- Query executions
- Support ticket creations

### Deployment

The application is ready for deployment to:
- Hugging Face Spaces (recommended)
- Streamlit Cloud
- Local server

See `DEPLOYMENT.md` for detailed instructions.

### Usage Example

1. Start the application: `streamlit run app.py`
2. View business dashboard in sidebar
3. Ask questions like:
   - "What are the top 5 products by sales?"
   - "Show me sales by region"
   - "Which customer has the highest spending?"
4. Request support tickets when needed
5. View console logs for agent operations

### Next Steps

1. Deploy to Hugging Face Spaces
2. Update `DEPLOYMENT_LINK.md` with actual deployment URL
3. Add screenshots to README (as per requirements)
4. Test all features in production environment

### Notes

- Screenshots should be added to the `screenshots/` directory and referenced in README.md
- GitHub credentials are optional - support tickets work in mock mode without them
- Database auto-initializes on first run if not present

---

**Status**: ✅ Complete and ready for deployment
**Last Updated**: [Current Date]

