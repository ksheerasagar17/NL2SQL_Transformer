import re
import requests
import json

OLLAMA_API_URL = "http://localhost:11434/api/generate"

SYSTEM_PROMPT = """You are an expert SQL developer. Convert natural language queries to SQL.
The database has the following schema:

Products Table:
- product_id (INTEGER PRIMARY KEY)
- name (TEXT)
- description (TEXT)
- price (DECIMAL)
- category (TEXT)
- stock_quantity (INTEGER)

Customers Table:
- customer_id (INTEGER PRIMARY KEY)
- name (TEXT)
- email (TEXT)
- join_date (DATE)
- total_orders (INTEGER)

Orders Table:
- order_id (INTEGER PRIMARY KEY)
- customer_id (INTEGER, FOREIGN KEY to customers.customer_id)
- order_date (DATETIME)
- total_amount (DECIMAL)
- status (TEXT)

Order Items Table:
- order_item_id (INTEGER PRIMARY KEY)
- order_id (INTEGER, FOREIGN KEY to orders.order_id)
- product_id (INTEGER, FOREIGN KEY to products.product_id)
- quantity (INTEGER)
- price_at_time (DECIMAL)

Example: To get top selling products, join products with order_items:
SELECT p.name, SUM(oi.quantity) as total_sold 
FROM products p 
JOIN order_items oi ON p.product_id = oi.product_id 
GROUP BY p.product_id, p.name;

Convert the user's natural language query to a valid SQL query.
Only return the SQL query, nothing else.
Ensure the query is safe and doesn't include any harmful operations.
Use appropriate JOINs when needed to relate data across tables."""

def sanitize_query(query: str) -> str:
    """Remove any potentially harmful SQL commands"""
    # Remove comments
    query = re.sub(r'--.*$', '', query, flags=re.MULTILINE)
    query = re.sub(r'/\*.*?\*/', '', query, flags=re.DOTALL)
    
    # Block dangerous keywords
    dangerous_keywords = [
        'DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER', 'TRUNCATE', 'REPLACE',
        'RESTORE', 'LOAD', 'CALL', 'EXEC', 'EXECUTE'
    ]
    
    for keyword in dangerous_keywords:
        if re.search(rf'\b{keyword}\b', query.upper()):
            raise ValueError(f"Unauthorized SQL command detected: {keyword}")
    
    return query.strip()

def validate_query(query: str) -> bool:
    """Basic validation of the SQL query"""
    # Check if it's a SELECT statement
    if not query.upper().startswith('SELECT'):
        raise ValueError("Only SELECT queries are allowed")
    
    # Check for basic SQL injection patterns
    # Only check for dangerous patterns
    dangerous_patterns = [
        r';\s*DROP',      # Drop tables
        r';\s*DELETE',    # Delete data
        r';\s*UPDATE',    # Update data
        r';\s*INSERT',    # Insert data
        r'INTO\s+OUTFILE',# File operations
        r'INTO\s+DUMP'    # Dump operations
    ]
    
    for pattern in dangerous_patterns:
        if re.search(pattern, query.upper()):
            raise ValueError("Query contains potentially harmful patterns")
    
    return True

def convert_to_sql(natural_query: str) -> str:
    """Convert natural language query to SQL using Ollama"""
    try:
        # Construct the prompt
        full_prompt = f"{SYSTEM_PROMPT}\n\nUser Query: {natural_query}\n\nSQL Query:"
        
        # Prepare the request to Ollama
        payload = {
            "model": "codellama",
            "prompt": full_prompt,
            "temperature": 0.1,
            "stream": False,
            "system": "You are an expert SQL developer. Only return valid SQL queries, no explanations."
        }
        
        # Make the request to Ollama
        response = requests.post(OLLAMA_API_URL, json=payload)
        
        if response.status_code != 200:
            raise ValueError(f"Ollama API error: {response.text}")
            
        # Extract the response
        response_data = response.json()
        sql_query = response_data['response'].strip()
        
        # Remove any markdown formatting
        sql_query = re.sub(r'```sql\s*|\s*```', '', sql_query)
        sql_query = sql_query.strip()
        
        # Sanitize and validate the query
        sql_query = sanitize_query(sql_query)
        validate_query(sql_query)
        
        return sql_query
    
    except requests.exceptions.ConnectionError:
        raise ValueError("Could not connect to Ollama. Make sure Ollama is running on localhost:11434")
    except Exception as e:
        raise ValueError(f"Error converting to SQL: {str(e)}")

if __name__ == '__main__':
    # Test the conversion
    test_queries = [
        "Show all products with price less than $50",
        "What are the top 5 customers by total orders?",
        "List all orders delivered in February 2024"
    ]
    
    for query in test_queries:
        try:
            sql = convert_to_sql(query)
            print(f"\nNatural Query: {query}")
            print(f"SQL Query: {sql}\n")
        except Exception as e:
            print(f"Error: {e}")
