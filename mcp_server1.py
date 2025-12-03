import os
import asyncio
import json
from dotenv import load_dotenv
from openai import OpenAI
from openai import APIError 

from fastmcp import FastMCP

from db_connector import execute_db_query, get_db_schema 

# Loading environment variables from .env file
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# OpenRouter Configuration 
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# headers for OpenRouter 
DEFAULT_HEADERS = {
    "HTTP-Referer": "https://mcp-server-test.com", 
    "X-Title": "FastMCP DB Tester" 
}
# Initializing MCP Server 
mcp = FastMCP("Database_OpenRouter_Tool", json_response=True)


# tool definition for Model 
@mcp.tool()
def get_database_schema() -> str:
    """
    Use this tool to get the structure of the SQLite database.

    
    Returns:
        The SQL Data Definition Language (DDL) for all tables.
    """
    return get_db_schema()

@mcp.tool()
def query_database(sql_query: str) -> str:
    """
    Executes a read-only SQL query against the SQLite database.
    
    

    Returns:
        The result of the SQL query as a JSON string, or an error message.
    """
    return execute_db_query(sql_query)


# Main Application Logic 
async def run_openrouter_chat(prompt: str):
    """
    The main function to send the user's prompt to OpenRouter, enabling it to use the MCP tools.
    """
    if not OPENROUTER_API_KEY:
        print("Error: OPENROUTER_API_KEY is not set in the .env file.")
        return

    # Initializing the OpenAI Client pointing to OpenRouter
    client = OpenAI(
        api_key=OPENROUTER_API_KEY,
        base_url=OPENROUTER_BASE_URL,
        default_headers=DEFAULT_HEADERS,
        timeout=120.0 
    )
    

    raw_tool_objects = await mcp.get_tools() 
    
    
    tool_declarations = []
    tool_function_map = {} 

    for tool_obj in raw_tool_objects.values():
        
        
        if not hasattr(tool_obj, 'name') or not hasattr(tool_obj, 'description') or not hasattr(tool_obj, 'parameters') or not hasattr(tool_obj, 'fn'):
            print(f"Error: Tool object is missing required execution attributes (name/fn). Cannot proceed.")
            return 
        
        
        function_schema = {
            "name": tool_obj.name,
            "description": tool_obj.description,
            "parameters": tool_obj.parameters
        }
        tool_declarations.append({"type": "function", "function": function_schema})
        
       
        tool_function_map[tool_obj.name] = tool_obj.fn 


    
    messages = [{"role": "user", "content": prompt}]

    
    print(f"\n--- User Prompt ---\n{prompt}")
    
    try:
        # Initial calling the API
        response = client.chat.completions.create(
            model="openai/gpt-3.5-turbo", 
            messages=messages,
            tools=tool_declarations 
        )
        
    except APIError as e:
        # API ERROR HANDLING 
        print("\n" + "="*50)
        print("FATAL API ERROR !!!")
        print("="*50)
        print(f"\n API Status Code: {e.status_code}")
        print(f"Details: {e.message}")
        print("Check your OpenRouter API Key, quota, and model name.")
        print("="*50 + "\n")
        return 
    
    # Function Calling Loop 
    while response.choices[0].message.tool_calls:
        
        messages.append(response.choices[0].message) 
        
        tool_outputs = []
        for call in response.choices[0].message.tool_calls:
            tool_name = call.function.name
            tool_args_str = call.function.arguments 
            tool_call_id = call.id
            
            print(f"\n--- Model Requested Tool: {tool_name} ---")
            print(f"Arguments (Raw String): {tool_args_str}")
            
            
            tool_func = tool_function_map.get(tool_name) 
            
            if tool_func:
                try:
                    
                    parsed_args = json.loads(tool_args_str) 
                except json.JSONDecodeError as json_e:
                    print(f"Error parsing JSON arguments for {tool_name}: {json_e}")
                    result = f"Error: Arguments for {tool_name} were malformed JSON: {tool_args_str}"
                    parsed_args = {}
                    
                
                
                result = tool_func(**parsed_args)
                    
                
                print(f"Tool Execution Result: {result[:100]}...")
                
                tool_outputs.append(
                    {
                        "tool_call_id": tool_call_id,
                        "role": "tool",
                        "name": tool_name,
                        "content": result,
                    }
                )
            else:
                print(f"Error: Tool '{tool_name}' not found in the function map.")
        
        messages.extend(tool_outputs)
        
        try:
            response = client.chat.completions.create(
                model="openai/gpt-3.5-turbo",
                messages=messages,
                tools=tool_declarations
            )
        except APIError as e:
            print(f"\nAPI Error during follow-up call: {e.status_code}. Unable to proceed.")
            return

    
    print("\n--- Final Model Response ---")
    print(response.choices[0].message.content)


if __name__ == '__main__':

    # Asking user for the prompt
    print("\n--- Interactive DB Query Agent ---")
    user_prompt = input("Enter your database query prompt: ")
    
    # Run the main async function
    asyncio.run(run_openrouter_chat(user_prompt))
