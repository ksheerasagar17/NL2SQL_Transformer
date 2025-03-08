# E-commerce Application Flow

```mermaid
graph LR
A((UI)) --> B[API]
B --> C[NL2SQL]
C --> D[DB]
D --> E[(Database)]
E --> D
D --> B
B --> A
```

## Simple Flow Description
- User interface sends queries to API
- API processes and sends to NL2SQL converter
- Converted SQL queries go to database handler
- Database executes and returns results
- Results flow back to user through the same path
