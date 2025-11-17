"""
AI Agent with function calling capabilities for database queries and support tickets.
Includes safety features to prevent dangerous operations.
"""
import os
import logging
from typing import List, Dict, Any, Optional, Tuple
from openai import OpenAI
from dotenv import load_dotenv
from database import execute_query, get_table_info
from github_ticket import create_github_issue

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Dangerous SQL keywords that should be blocked
DANGEROUS_KEYWORDS = [
    'DROP', 'DELETE', 'TRUNCATE', 'ALTER', 'CREATE', 'INSERT', 'UPDATE',
    'EXEC', 'EXECUTE', 'GRANT', 'REVOKE', 'MERGE', 'REPLACE'
]


class DataInsightsAgent:
    """AI Agent for querying database and managing support tickets."""
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4"  # or "gpt-3.5-turbo" for faster/cheaper
        self.conversation_history = []
        
    def _check_query_safety(self, query: str) -> Tuple[bool, Optional[str]]:
        """Check if query contains dangerous operations."""
        query_upper = query.upper().strip()
        
        # Only allow SELECT queries
        if not query_upper.startswith('SELECT'):
            return False, "Only SELECT queries are allowed for safety."
        
        # Check for dangerous keywords
        for keyword in DANGEROUS_KEYWORDS:
            if keyword in query_upper:
                return False, f"Operation '{keyword}' is not allowed for safety reasons."
        
        return True, None
    
    def query_database(self, query: str) -> Dict[str, Any]:
        """
        Execute a safe SELECT query on the database.
        
        Args:
            query: SQL SELECT query string
            
        Returns:
            Dictionary with query results or error message
        """
        logger.info(f"Received database query: {query}")
        
        # Safety check
        is_safe, error_msg = self._check_query_safety(query)
        if not is_safe:
            logger.warning(f"Blocked dangerous query: {query}")
            return {
                "success": False,
                "error": error_msg,
                "data": None
            }
        
        try:
            results = execute_query(query)
            logger.info(f"Query executed successfully. Returned {len(results)} rows")
            return {
                "success": True,
                "data": results,
                "row_count": len(results)
            }
        except Exception as e:
            logger.error(f"Query execution error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "data": None
            }
    
    def create_support_ticket(self, title: str, description: str, labels: List[str] = None) -> Dict[str, Any]:
        """
        Create a support ticket in GitHub Issues.
        
        Args:
            title: Title of the support ticket
            description: Description of the issue
            labels: Optional list of labels for the issue
            
        Returns:
            Dictionary with ticket creation result
        """
        logger.info(f"Creating support ticket: {title}")
        
        try:
            result = create_github_issue(title, description, labels or [])
            if result.get("success"):
                logger.info(f"Support ticket created: {result.get('url')}")
            else:
                logger.error(f"Failed to create ticket: {result.get('error')}")
            return result
        except Exception as e:
            logger.error(f"Error creating support ticket: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "url": None
            }
    
    def get_available_functions(self) -> List[Dict[str, Any]]:
        """Get list of available functions for the agent."""
        return [
            {
                "type": "function",
                "function": {
                    "name": "query_database",
                    "description": "Execute a safe SELECT query on the sales database. Only SELECT queries are allowed. Returns query results as a list of dictionaries.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "SQL SELECT query to execute. Must be a SELECT statement only."
                            }
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "create_support_ticket",
                    "description": "Create a support ticket in GitHub Issues. Use this function when: 1) The user explicitly asks to create a support ticket, 2) The user asks to 'create a ticket', 'file a ticket', 'open a ticket', or similar phrases, 3) The user needs human assistance that cannot be resolved automatically, 4) The user reports a bug or issue. ALWAYS use this function when the user explicitly requests a support ticket.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "Title of the support ticket. Should be a concise summary of the issue."
                            },
                            "description": {
                                "type": "string",
                                "description": "Detailed description of the issue or question. Include any relevant context from the conversation."
                            },
                            "labels": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Optional labels for categorizing the ticket (e.g., 'bug', 'question', 'feature-request', 'support')"
                            }
                        },
                        "required": ["title", "description"]
                    }
                }
            }
        ]
    
    def chat(self, user_message: str) -> str:
        """
        Process user message and return agent response.
        
        Args:
            user_message: User's input message
            
        Returns:
            Agent's response text
        """
        logger.info(f"User message: {user_message}")
        
        # Check if user explicitly requested a support ticket
        user_message_lower = user_message.lower()
        ticket_keywords = ["create a support ticket", "create support ticket", "file a ticket", 
                          "open a ticket", "create a ticket", "support ticket", "file ticket"]
        force_ticket = any(keyword in user_message_lower for keyword in ticket_keywords)
        
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Prepare messages for API call
        messages = [
            {
                "role": "system",
                "content": """You are a helpful AI assistant for a Data Insights application. 
Your role is to help users query and understand sales data from a database.

IMPORTANT GUIDELINES:
1. You can only execute SELECT queries - never DELETE, DROP, UPDATE, INSERT, or any other modifying operations
2. When users ask complex questions, break them down into SQL queries using the query_database function
3. If a user explicitly asks to "create a support ticket", "file a ticket", "open a ticket", or similar phrases, you MUST use the create_support_ticket function immediately
4. Always explain your findings in a clear, business-friendly manner
5. If query results are large, summarize the key insights rather than listing all rows
6. When a user reports an issue or problem, use the create_support_ticket function to help them
7. You have access to the create_support_ticket function - use it whenever the user requests a ticket or reports an issue

Available tables:
- sales: Contains sales transactions with columns: id, date, customer, product, category, quantity, unit_price, total_amount, region, sales_rep
- customers: Contains customer information with columns: id, name, region, contact_email, total_orders, total_spent

Available functions:
- query_database: Execute SELECT queries on the database
- create_support_ticket: Create a GitHub issue for support requests (USE THIS when user asks for a ticket)

Be helpful, accurate, and safety-conscious. Always use the create_support_ticket function when explicitly requested."""
            }
        ] + self.conversation_history
        
        # Determine tool choice - force function call if ticket requested
        tool_choice = "auto"
        if force_ticket:
            tool_choice = {"type": "function", "function": {"name": "create_support_ticket"}}
            logger.info("Forcing support ticket creation based on user request")
        
        # Call OpenAI API with function calling
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.get_available_functions(),
                tool_choice=tool_choice
            )
            
            message = response.choices[0].message
            logger.info(f"Assistant response: {message.content}")
            
            # If forcing ticket but no tool calls, create ticket directly
            if force_ticket and not message.tool_calls:
                logger.info("Forced ticket creation but no tool call received, creating ticket directly")
                # Extract title and description from user message
                title = user_message.split("for")[-1].strip() if "for" in user_message else "Support Request"
                if not title or len(title) < 5:
                    title = "Support Request"
                description = user_message
                
                result = self.create_support_ticket(title=title, description=description, labels=["support"])
                # Format response
                if result.get("success"):
                    url = result.get("url", "N/A")
                    return f"I've created a support ticket for you!\n\n**Title:** {title}\n**Ticket URL:** {url}\n\nThe support team will review your request and get back to you soon."
                else:
                    error = result.get("error", "Unknown error")
                    return f"I attempted to create a support ticket, but encountered an issue: {error}. Please try again or contact support directly."
            
            # Handle function calls
            if message.tool_calls:
                for tool_call in message.tool_calls:
                    function_name = tool_call.function.name
                    import json
                    function_args = json.loads(tool_call.function.arguments)
                    
                    logger.info(f"Calling function: {function_name} with args: {function_args}")
                    
                    if function_name == "query_database":
                        result = self.query_database(**function_args)
                        # Add function result to conversation
                        self.conversation_history.append({
                            "role": "assistant",
                            "content": message.content,
                            "tool_calls": [
                                {
                                    "id": tool_call.id,
                                    "type": "function",
                                    "function": {
                                        "name": function_name,
                                        "arguments": tool_call.function.arguments
                                    }
                                }
                            ]
                        })
                        self.conversation_history.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": json.dumps(result)
                        })
                    elif function_name == "create_support_ticket":
                        result = self.create_support_ticket(**function_args)
                        self.conversation_history.append({
                            "role": "assistant",
                            "content": message.content,
                            "tool_calls": [
                                {
                                    "id": tool_call.id,
                                    "type": "function",
                                    "function": {
                                        "name": function_name,
                                        "arguments": tool_call.function.arguments
                                    }
                                }
                            ]
                        })
                        self.conversation_history.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": json.dumps(result)
                        })
                
                # Get final response after function execution
                messages = [
                    {
                        "role": "system",
                        "content": """You are a helpful AI assistant for a Data Insights application. 
Your role is to help users query and understand sales data from a database.

When you receive function results:
- For create_support_ticket: If the result shows success=True and includes a URL, inform the user that the support ticket was created successfully and provide the URL. If success=False, explain the issue but still confirm you attempted to create the ticket.
- For query_database: Present the query results in a clear, business-friendly format."""
                    }
                ] + self.conversation_history
                
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages
                )
                message = response.choices[0].message
            
            # Add assistant response to history
            assistant_response = message.content or "I've processed your request."
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_response
            })
            
            return assistant_response
            
        except Exception as e:
            logger.error(f"Error in chat: {str(e)}")
            return f"I encountered an error: {str(e)}. Would you like me to create a support ticket for this issue?"
    
    def reset_conversation(self):
        """Reset conversation history."""
        self.conversation_history = []
        logger.info("Conversation history reset")

