# Intacct REST SDK for Python

A Python SDK for the Sage Intacct REST API, providing a simple and intuitive interface to interact with Intacct's financial data and operations.

## Local Setup

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# Install dev dependencies
pip install -r requirements.txt
```

## Quick Start

### 1. Authentication Setup

First, you'll need to set up OAuth2 credentials with Intacct:

1. Register your application in Intacct to get `client_id` and `client_secret`
2. Set up environment variables or pass credentials directly

```python
import os
from intacctsdk import IntacctRESTSDK

sdk = IntacctRESTSDK(
    refresh_token='your_refresh_token',
    entity_id='your_entity_id'  # Optional
)
```

### 2. Basic Usage

For comprehensive examples and usage patterns, see the [`example.py`](example.py) file which demonstrates:

- OAuth2 authentication flow
- Working with different modules dimensions
- Filtering and querying data
- Error handling
- Token management

### Common Methods

All API classes inherit from `ApiBase` and support these common methods:

#### `get_all_generator(fields, filters=[], filter_expression=None, order_by=[], dimension_name=None)`
Returns a generator that yields paginated results.

**Parameters:**
- `fields` (List[str]): List of fields to retrieve
- `filters` (List[Dict], optional): Filter conditions
- `filter_expression` (str, optional): Filter expression ('and' or 'or')
- `order_by` (List[Dict], optional): Sort conditions
- `dimension_name` (str, optional): For dimensions API only

#### `get_by_id(id)`
Get a single object by its ID.

#### `count(filters=[], filter_expression=None, dimension_name=None)`
Get the count of objects matching the filters.

#### `get_model()`
Get the schema/model definition for the object type.


## Error Handling

The SDK provides custom exceptions for different error scenarios:

```python
from intacctsdk.exceptions import InvalidTokenError, BadRequestError, InternalServerError

try:
    accounts = list(sdk.accounts.get_all_generator(fields=['id', 'name']))
except InvalidTokenError as e:
    print(f"Token error: {e.message}")
    # Handle token refresh or re-authentication
except BadRequestError as e:
    print(f"Bad request: {e.message}")
    # Handle invalid parameters or request format
except InternalServerError as e:
    print(f"Server error: {e.message}")
    # Handle temporary server issues
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
