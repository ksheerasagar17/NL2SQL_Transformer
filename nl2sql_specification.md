# NL2SQL Implementation Specification

## 1. Class Structure

### 1.1 TextPreprocessor
```python
class TextPreprocessor:
    def tokenize(self, text: str) -> List[str]
    def remove_stopwords(self, tokens: List[str]) -> List[str]
    def lemmatize(self, tokens: List[str]) -> List[str]
    def extract_entities(self, text: str) -> Dict[str, Any]
```

### 1.2 ContextAnalyzer
```python
class ContextAnalyzer:
    def classify_intent(self, preprocessed_text: Dict) -> str
    def extract_entities(self, preprocessed_text: Dict) -> List[Entity]
    def map_relationships(self, entities: List[Entity]) -> Dict[str, Relationship]
```

### 1.3 SchemaManager
```python
class SchemaManager:
    def validate_schema(self, table_name: str) -> bool
    def get_column_metadata(self, table_name: str) -> List[ColumnMetadata]
    def resolve_table_relationships(self, tables: List[str]) -> List[Relationship]
```

### 1.4 QueryBuilder
```python
class QueryBuilder:
    def generate_select_query(self, params: QueryParams) -> str
    def generate_insert_query(self, params: QueryParams) -> str
    def generate_update_query(self, params: QueryParams) -> str
    def generate_delete_query(self, params: QueryParams) -> str
```

### 1.5 QueryValidator
```python
class QueryValidator:
    def validate_syntax(self, query: str) -> bool
    def check_security(self, query: str) -> SecurityReport
    def optimize_query(self, query: str) -> str
```

## 2. Data Models

### 2.1 Entity Model
```python
@dataclass
class Entity:
    name: str
    type: str
    value: Any
    confidence: float
```

### 2.2 QueryParams Model
```python
@dataclass
class QueryParams:
    query_type: str
    table_name: str
    columns: List[str]
    conditions: List[Condition]
    joins: List[Join]
    limit: Optional[int]
    order_by: Optional[List[str]]
```

### 2.3 DatabaseSchema Model
```python
@dataclass
class ColumnMetadata:
    name: str
    data_type: str
    is_nullable: bool
    is_primary: bool
    foreign_key: Optional[str]
```

## 3. Configuration

### 3.1 Database Configuration
```python
DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'ecommerce',
    'user': 'db_user',
    'password': 'db_password'
}
```

### 3.2 NL2SQL Configuration
```python
NL2SQL_CONFIG = {
    'max_token_length': 100,
    'min_confidence_score': 0.75,
    'timeout_seconds': 30,
    'cache_schema': True,
    'max_query_complexity': 10
}
```

## 4. API Endpoints

### 4.1 Query Endpoint
```python
@app.route('/api/nl2sql', methods=['POST'])
def process_natural_language_query():
    """
    Request Body:
    {
        "query": "Show all orders from last week",
        "user_id": "user123",
        "context": {
            "tables": ["orders", "users"],
            "filters": {}
        }
    }

    Response:
    {
        "sql": "SELECT * FROM orders WHERE...",
        "params": [...],
        "metadata": {
            "tables_accessed": [...],
            "execution_time": "0.123s"
        }
    }
    """
```

## 5. Error Handling

```python
class NL2SQLError(Exception):
    def __init__(self, message: str, error_code: str, details: Dict = None):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
```

### 5.1 Error Codes
```python
ERROR_CODES = {
    'INVALID_QUERY': 'E001',
    'SCHEMA_ERROR': 'E002',
    'SECURITY_VIOLATION': 'E003',
    'TIMEOUT_ERROR': 'E004',
    'PARSING_ERROR': 'E005'
}
```

## 6. Security Implementation

```python
class SecurityManager:
    def sanitize_input(self, query: str) -> str
    def validate_access_rights(self, user_id: str, tables: List[str]) -> bool
    def check_query_complexity(self, query: str) -> ComplexityScore
```

## 7. Testing Guidelines

### 7.1 Unit Tests
```python
def test_text_preprocessing():
    preprocessor = TextPreprocessor()
    result = preprocessor.tokenize("Show all orders")
    assert len(result) > 0
    assert "orders" in result

def test_query_generation():
    builder = QueryBuilder()
    params = QueryParams(...)
    query = builder.generate_select_query(params)
    assert "SELECT" in query
    assert "FROM" in query
```

### 7.2 Integration Tests
```python
def test_end_to_end_query():
    nl2sql = NL2SQLProcessor()
    result = nl2sql.process("Show all orders from last week")
    assert result.sql is not None
    assert result.success is True
```

## 8. Performance Considerations

1. Query Optimization
   - Implement query caching
   - Use prepared statements
   - Index frequently accessed columns

2. Schema Caching
   - Cache database schema
   - Implement schema version tracking
   - Periodic schema refresh

3. Connection Pooling
   - Maintain connection pool
   - Handle connection timeout
   - Implement retry logic

## 9. Deployment Requirements

```yaml
dependencies:
  - python: ">=3.8"
  - nltk: ">=3.6"
  - sqlalchemy: ">=1.4"
  - spacy: ">=3.0"
  - flask: ">=2.0"
  - psycopg2: ">=2.9"

environment:
  - PYTHONPATH: "/app"
  - DATABASE_URL: "postgresql://..."
  - LOG_LEVEL: "INFO"
```

## 10. Logging Strategy

```python
import logging

logging.config.dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }
    },
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'nl2sql.log',
            'formatter': 'default',
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['file']
    }
})
