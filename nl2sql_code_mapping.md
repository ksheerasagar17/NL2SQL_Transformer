# NL2SQL Code Mapping Document

## 1. Component Dependencies
```
TextPreprocessor
    ↓
ContextAnalyzer
    ↓
SchemaManager ←→ DatabaseConnector
    ↓
QueryBuilder
    ↓
QueryValidator → SecurityManager
```

## 2. Data Flow Mapping

### 2.1 Request Processing Pipeline
```
Input: "Show all orders from last week"
│
├─► TextPreprocessor
│   └─► tokens[] = ["show", "orders", "last", "week"]
│
├─► ContextAnalyzer
│   ├─► intent = "SELECT"
│   └─► entities = {
│       "table": "orders",
│       "timeframe": "last_week"
│     }
│
├─► SchemaManager
│   ├─► validateTable("orders")
│   └─► getColumns("orders")
│
├─► QueryBuilder
│   └─► SQL Template Population
│
└─► QueryValidator
    ├─► Syntax Check
    └─► Security Validation
```

## 3. File Organization

```
src/
├── preprocessor/
│   ├── __init__.py
│   ├── tokenizer.py
│   ├── stopwords.py
│   └── entity_extractor.py
│
├── analyzer/
│   ├── __init__.py
│   ├── context.py
│   ├── intent.py
│   └── relationships.py
│
├── database/
│   ├── __init__.py
│   ├── schema.py
│   ├── connector.py
│   └── metadata.py
│
├── query/
│   ├── __init__.py
│   ├── builder.py
│   ├── validator.py
│   └── optimizer.py
│
├── security/
│   ├── __init__.py
│   ├── sanitizer.py
│   └── access_control.py
│
└── utils/
    ├── __init__.py
    ├── logger.py
    └── config.py
```

## 4. Class Dependencies

```
TextPreprocessor
    → NLTK Tokenizer
    → SpaCy NER
    → Custom Stopwords List

ContextAnalyzer
    → Intent Classifier
    → Entity Recognizer
    → Relationship Mapper

SchemaManager
    → Database Connector
    → Metadata Cache
    → Relationship Registry

QueryBuilder
    → Template Engine
    → Parameter Binder
    → SQL Generator

QueryValidator
    → Syntax Checker
    → Security Manager
    → Query Optimizer
```

## 5. Configuration Dependencies

```
config/
├── database.yaml   → DatabaseConnector
├── nlp.yaml       → TextPreprocessor
├── security.yaml  → SecurityManager
├── api.yaml       → APIHandler
└── logging.yaml   → Logger
```

## 6. Integration Points

### 6.1 External Systems
```
NL2SQL System
    ↔ Database System (PostgreSQL)
    ↔ Authentication Service
    ↔ Monitoring System
    ↔ Logging Service
```

### 6.2 Internal Communication
```
Components         Events/Messages
─────────────     ──────────────────────
Preprocessor   →   TokenizedText
Analyzer      →   QueryIntent
SchemaManager →   TableMetadata
QueryBuilder  →   SQLQuery
Validator     →   ValidationResult
```

## 7. Error Handling Flow

```
User Input Error
    → TextPreprocessor.tokenize()
    → ERROR_CODES.PARSING_ERROR

Schema Error
    → SchemaManager.validate()
    → ERROR_CODES.SCHEMA_ERROR

Security Error
    → SecurityManager.validate()
    → ERROR_CODES.SECURITY_VIOLATION

Query Error
    → QueryBuilder.generate()
    → ERROR_CODES.INVALID_QUERY

Timeout Error
    → Any Component
    → ERROR_CODES.TIMEOUT_ERROR
```

## 8. Test Coverage Mapping

```
Unit Tests
├── preprocessor_tests/
│   ├── test_tokenizer.py
│   └── test_entity_extractor.py
│
├── analyzer_tests/
│   ├── test_context.py
│   └── test_intent.py
│
└── query_tests/
    ├── test_builder.py
    └── test_validator.py

Integration Tests
├── test_full_pipeline.py
└── test_error_handling.py

Performance Tests
├── test_query_performance.py
└── test_concurrent_requests.py
```

## 9. Deployment Pipeline

```
Source Code
    ↓
Linting (flake8, mypy)
    ↓
Unit Tests
    ↓
Integration Tests
    ↓
Build Package
    ↓
Deploy to Staging
    ↓
Performance Tests
    ↓
Security Scan
    ↓
Deploy to Production
```

## 10. Monitoring Points

```
Performance Metrics
├── Preprocessing Time
├── Query Generation Time
├── Database Response Time
└── Total Request Time

Error Metrics
├── Parse Failures
├── Schema Validation Failures
├── Security Violations
└── Timeout Events

Resource Metrics
├── Memory Usage
├── CPU Usage
├── Database Connections
└── Cache Hit Ratio
