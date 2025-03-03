#!/usr/bin/env python
"""
Validate the OpenAPI specification using openapi-spec-validator.
"""
import sys
import os
import yaml
from openapi_spec_validator import validate_spec


def load_yaml_file(file_path):
    """Load a YAML file and return its contents."""
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


def validate_openapi_spec(file_path):
    """Validate an OpenAPI specification file."""
    try:
        spec_dict = load_yaml_file(file_path)
        validate_spec(spec_dict)
        print(f"✅ OpenAPI specification is valid: {file_path}")
        return True
    except Exception as e:
        print(f"❌ OpenAPI specification validation failed: {file_path}")
        print(f"Error: {str(e)}")
        return False


if __name__ == "__main__":
    # Get the file path from command line arguments or use default
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        # Default to the openapi.yaml in the same directory as this script
        file_path = os.path.join(os.path.dirname(__file__), "openapi.yaml")
    
    # Validate the specification
    is_valid = validate_openapi_spec(file_path)
    
    # Exit with appropriate status code
    sys.exit(0 if is_valid else 1) 