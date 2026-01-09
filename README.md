# Distributed Rate Limit

This project implements a distributed rate limiter in Python using the **Fixed Window** algorithm backed by **Redis**. It allows you to limit the number of actions a user (or any unique identifier) can perform within a specified time window.

## Features

- **Distributed**: Uses Redis to store request counts, making it suitable for distributed systems where multiple application instances share the same rate limit.
- **Fixed Window Algorithm**: Simple and effective approach for rate limiting.
- **Atomic Operations**: Uses Redis pipelines to ensure the counter increment and expiration are handled correctly.

## Prerequisites

- Python 3.x
- Redis server (running locally or accessible remotely)
- (Optional) `fakeredis` for testing without a real Redis server.

## Installation

1. Clone the repository.
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Here is a simple example of how to use the `FixedWindowRateLimiter`:

```python
import redis
import time
from rate_limiter import FixedWindowRateLimiter

# 1. Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# 2. Initialize the Rate Limiter
# Allow 100 requests per minute (60 seconds)
limiter = FixedWindowRateLimiter(redis_client=r, limit=100, window_size_seconds=60)

user_id = "user_123"

# 3. Check if request is allowed
if limiter.is_allowed(user_id):
    print("Request allowed")
    # Process request...
else:
    print("Rate limit exceeded")
```

## Running Tests

An example test script is provided in `test_limiter.py`. It simulates requests to demonstrate the blocking behavior.

```bash
python test_limiter.py
```

It will attempt to connect to a local Redis instance. If unavailable, it will try to use `fakeredis` if installed.

## Project Structure

- `rate_limiter.py`: Contains the `FixedWindowRateLimiter` class implementation.
- `test_limiter.py`: A script to test and demonstrate the rate limiter.
- `requirements.txt`: List of Python dependencies.
