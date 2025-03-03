# Creating and Maintaining OpenAPI Specifications

This guide provides instructions on how to create, validate, and maintain OpenAPI specifications for the Bitcoin Wallet Tracker project.

## What is OpenAPI?

OpenAPI (formerly known as Swagger) is a specification for describing RESTful APIs. It allows you to define your API in a standardized way, making it easier to document, test, and generate client libraries.

## Creating an OpenAPI Specification

### Basic Structure

An OpenAPI specification is a YAML or JSON file with a specific structure. Here's a basic template:

```yaml
openapi: 3.0.3
info:
  title: API Title
  description: API Description
  version: 1.0.0
servers:
  - url: http://api.example.com/v1
    description: Production server
paths:
  /resource:
    get:
      summary: Get a resource
      responses:
        '200':
          description: Successful response
components:
  schemas:
    Resource:
      type: object
      properties:
        id:
          type: integer
```

### Key Components

1. **Info**: Basic metadata about your API
2. **Servers**: The servers where your API is hosted
3. **Paths**: The endpoints of your API
4. **Components**: Reusable components like schemas, parameters, and responses

## Validating the Specification

We've provided a validation script in `docs/validate_openapi.py`. To use it:

1. Install the required dependencies:
   ```bash
   pip install -r requirements/local.txt
   ```

2. Run the validation script:
   ```bash
   python docs/validate_openapi.py
   ```

## Maintaining the Specification

As your API evolves, you should keep your OpenAPI specification up to date:

1. **Add new endpoints**: When you add a new endpoint to your API, add it to the `paths` section
2. **Update existing endpoints**: When you change an existing endpoint, update its definition
3. **Add new models**: When you add a new model, add it to the `components/schemas` section
4. **Version your API**: When you make breaking changes, increment the version number

## Best Practices

1. **Be descriptive**: Include detailed descriptions for endpoints, parameters, and schemas
2. **Use examples**: Provide examples for request and response bodies
3. **Document all responses**: Include all possible response codes and their meanings
4. **Use tags**: Organize endpoints logically with tags
5. **Keep it DRY**: Use components to avoid repetition

## Tools for Working with OpenAPI

### Editors

- [Swagger Editor](https://editor.swagger.io/)
- [Stoplight Studio](https://stoplight.io/studio/)
- [VS Code with OpenAPI extension](https://marketplace.visualstudio.com/items?itemName=42Crunch.vscode-openapi)

### Documentation Generators

- [Swagger UI](https://swagger.io/tools/swagger-ui/)
- [ReDoc](https://github.com/Redocly/redoc)
- [Stoplight Elements](https://stoplight.io/open-source/elements)

### Code Generators

- [OpenAPI Generator](https://openapi-generator.tech/)
- [Swagger Codegen](https://github.com/swagger-api/swagger-codegen)

## Example: Adding a New Endpoint

Here's how to add a new endpoint to the OpenAPI specification:

1. Open `docs/openapi.yaml`
2. Add the new endpoint under the `paths` section:

```yaml
  /wallet/export/{id}/:
    get:
      summary: Export address transactions
      description: Export transactions for a specific Bitcoin address as CSV
      operationId: exportAddressTransactions
      tags:
        - addresses
      security:
        - cookieAuth: []
      parameters:
        - name: id
          in: path
          description: ID of the Bitcoin address
          required: true
          schema:
            type: integer
            format: int64
      responses:
        '200':
          description: CSV file with transactions
          content:
            text/csv:
              schema:
                type: string
                format: binary
        '401':
          description: Unauthorized
        '404':
          description: Address not found
```

3. Validate the updated specification:
   ```bash
   python docs/validate_openapi.py
   ```

## Resources

- [OpenAPI Specification](https://swagger.io/specification/)
- [OpenAPI Guide](https://swagger.io/docs/specification/about/)
- [OpenAPI Examples](https://github.com/OAI/OpenAPI-Specification/tree/main/examples/v3.0) 