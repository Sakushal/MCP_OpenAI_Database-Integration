# MCP OpenAI Database Integration

This project integrates an SQLite database with the OpenAI GPT-3.5 model using the **FastMCP** server framework. The main objective is to allow users to query a database through the OpenAI model using natural language.

With this setup, the **MCP** (Model-Controlled Prompting) server allows users to run SQL queries on an SQLite database via conversational AI prompts, interacting with the data seamlessly and in real-time.

## Features

- Connects to an SQLite database.
- Provides tools to query the database schema and run read-only SQL queries.
- Integrates the **OpenAI GPT-3.5** model for natural language understanding of database queries.
- Uses the **FastMCP** framework for easy model-tool interaction.
- Retrieves database schema information and executes SQL queries based on user input.

## Prerequisites

- Python 3.7+
- **OpenAI API Key** (Get it from [OpenAI](https://platform.openai.com/signup))
- SQLite database (.db file) to query.

## Setup and Installation

### 1. Clone the Repository

Clone the project to your local machine:

```bash
git clone https://github.com/Sakushal/MCP_OpenAI_Database-Integration.git
cd MCP_OpenAI_Database-Integration
```

### 2. Install Required Python Libraries

Create a virtual environment and activate it:

```bash
python3 -m venv .venv
source .venv/bin/activate    # On Linux/MacOS
.venv\Scripts\activate      # On Windows
```

Install the necessary dependencies:

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a .env file in the root of the project directory and add the following content:

```bash
OPENROUTER_API_KEY=your-openai-api-key-here
```

Replace 'your-openai-api-key-here' with your actual OpenAI API key.

### 4. Run the Application

Run the program using:

```bash
python mcp_server1.py

```

### 5. Interact with the Application

When you run the program, you will be prompted to enter a natural language related to the database. The OpenAI model will interpret your query and use the tools available to fetch or query the SQLite database.

```bash
"Show me all users who are older than 30 years"
```
This will generate the appropriate SQL query and return the results from the database.


## File Structure

MCP_OpenAI_Database-Integration/

├── .venv/

├── .gitignore

├── .env  

├── mcp.py     

├── db_connector.py        

├── requirements.txt        

└── README.md               

