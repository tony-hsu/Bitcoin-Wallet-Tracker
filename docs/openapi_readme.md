# OpenAPI Specification for Bitcoin Wallet Tracker

This directory contains the OpenAPI specification for the Bitcoin Wallet Tracker API. The specification is defined in the `openapi.yaml` file.

## What is OpenAPI?

OpenAPI (formerly known as Swagger) is a specification for describing RESTful APIs. It allows you to define your API in a standardized way, making it easier to document, test, and generate client libraries.

## Using the OpenAPI Specification

### Viewing the API Documentation

You can view the API documentation using Swagger UI or ReDoc. Here are some options:

1. **Online Swagger Editor**: 
   - Go to [Swagger Editor](https://editor.swagger.io/)
   - Import the `openapi.yaml` file

2. **Local Swagger UI**:
   - Install Swagger UI: `npm install -g swagger-ui-dist`
   - Serve the UI: `swagger-ui-dist serve -p 8080 openapi.yaml`

3. **ReDoc**:
   - Install ReDoc: `npm install -g redoc-cli`
   - Serve the documentation: `redoc-cli serve openapi.yaml`

### Generating Client Libraries

You can use the OpenAPI Generator to generate client libraries for various programming languages:

```bash
# Install OpenAPI Generator
npm install -g @openapitools/openapi-generator-cli

# Generate a Python client
openapi-generator-cli generate -i openapi.yaml -g python -o ./generated-clients/python

# Generate a JavaScript client
openapi-generator-cli generate -i openapi.yaml -g javascript -o ./generated-clients/javascript
```

### Testing the API

You can use tools like Postman or Insomnia to test the API:

1. **Postman**:
   - Import the OpenAPI specification
   - Postman will create a collection with all the endpoints

2. **Insomnia**:
   - Import the OpenAPI specification
   - Insomnia will create requests for all endpoints

## Customizing the Specification

Feel free to modify the `openapi.yaml` file to match your specific API requirements. The current specification is based on the existing Bitcoin Wallet Tracker application, but you may need to adjust it as your API evolves.

## Best Practices

1. Keep the specification up-to-date as your API changes
2. Use meaningful descriptions for endpoints, parameters, and schemas
3. Include examples for request and response bodies
4. Document all possible response codes
5. Use tags to organize endpoints logically

## Resources

- [OpenAPI Specification](https://swagger.io/specification/)
- [Swagger UI](https://swagger.io/tools/swagger-ui/)
- [ReDoc](https://github.com/Redocly/redoc)
- [OpenAPI Generator](https://openapi-generator.tech/) 