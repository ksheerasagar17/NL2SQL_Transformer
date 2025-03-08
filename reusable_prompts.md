# Reusable Prompts for NL2SQL Application Development

## 1. Flow Diagram Generation
```
write up a flow diagram for [APPLICATION_NAME] and make sure its simple to understand
```
Generates: High-level flow diagram showing component interactions

## 2. Detailed Architecture Document
```
write up a detailed nl2sql architecture document focusing on:
- Input Layer
- Processing Layer
- Output Layer
- Example Flow
- Key Components
- Security Considerations
```
Generates: Comprehensive architecture document with layer-by-layer breakdown

## 3. Code Specification
```
write up a coding specification document for [APPLICATION_NAME] including:
- Class Structures
- Data Models
- Configuration
- API Endpoints
- Error Handling
- Security Implementation
- Testing Guidelines
- Performance Considerations
- Deployment Requirements
- Logging Strategy
```
Generates: Detailed technical implementation specifications

## 4. Code Mapping Document
```
create a code mapping document that shows:
- Component Dependencies
- Data Flow Mapping
- File Organization
- Class Dependencies
- Configuration Dependencies
- Integration Points
- Error Handling Flow
- Test Coverage
- Deployment Pipeline
- Monitoring Points
```
Generates: Component integration and relationship documentation

## Parameters to Replace:
1. [APPLICATION_NAME]: Your application name
2. Database configuration:
   ```python
   DATABASE_CONFIG = {
       'host': '[DB_HOST]',
       'port': [DB_PORT],
       'database': '[DB_NAME]',
       'user': '[DB_USER]',
       'password': '[DB_PASSWORD]'
   }
   ```
3. API endpoints:
   ```python
   @app.route('[API_ENDPOINT]', methods=['[HTTP_METHOD]'])
   ```
4. Configuration paths:
   ```
   'PYTHONPATH': "[APP_PATH]"
   'DATABASE_URL': "[DB_CONNECTION_STRING]"
   ```
5. Logging paths:
   ```python
   'filename': '[LOG_FILE_PATH]'
   ```

## Usage Example:
To create similar documentation for a new application:

1. Replace [APPLICATION_NAME] with your app name, e.g., "Product Catalog Service"
2. Update database configurations with your values
3. Modify API endpoints to match your service routes
4. Adjust paths according to your project structure
5. Run the prompts in sequence to generate complete documentation

## Notes:
- Keep ASCII diagrams for maximum compatibility
- Adjust component names based on your application's needs
- Modify security considerations according to your requirements
- Update testing guidelines based on your tech stack
- Customize deployment pipeline for your infrastructure
