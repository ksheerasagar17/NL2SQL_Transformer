from flask import Flask, request, jsonify, render_template
from database import init_db, get_db_connection
from nl2sql import convert_to_sql
import sqlite3
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize database
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def process_query():
    try:
        data = request.get_json()
        natural_query = data.get('query')

        if not natural_query:
            return jsonify({'error': 'No query provided'}), 400

        # Convert natural language to SQL
        sql_query = convert_to_sql(natural_query)

        # Execute the query
        conn = get_db_connection()
        try:
            df = pd.read_sql_query(sql_query, conn)
            results = df.to_dict('records')
            
            return jsonify({
                'results': results,
                'sql_query': sql_query
            })
        except sqlite3.Error as e:
            return jsonify({'error': f'Database error: {str(e)}'}), 500
        finally:
            conn.close()

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/schema')
def get_schema():
    """Return the database schema for reference"""
    conn = get_db_connection()
    schema = {}
    
    try:
        cursor = conn.cursor()
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        for table in tables:
            table_name = table[0]
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            schema[table_name] = [
                {
                    'name': col[1],
                    'type': col[2]
                } for col in columns
            ]
        
        return jsonify(schema)
    except sqlite3.Error as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
