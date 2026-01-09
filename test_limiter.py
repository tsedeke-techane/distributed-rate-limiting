import redis
import time
import sys
from rate_limiter import FixedWindowRateLimiter

def main():
    # Connect to Redis
    try:
        # Attempt to connect to a local Redis instance
        r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        r.ping() # Check connection
        print("Connected to Redis successfully.")
    except redis.ConnectionError:
        print("Could not connect to real Redis. Falling back to fakeredis for demonstration.")
        try:
            import fakeredis
            r = fakeredis.FakeStrictRedis(decode_responses=True)
            print("Connected to FakeRedis successfully.")
        except ImportError:
            print("Error: Could not connect to Redis and fakeredis is not installed.")
            sys.exit(1)

    # Initialize rate limiter: 5 requests per 10 seconds (for faster testing)
    limit = 5
    window = 10
    limiter = FixedWindowRateLimiter(r, limit=limit, window_size_seconds=window)

    user_id = "user_123"
    print(f"Testing Rate Limiter: {limit} requests per {window} seconds for {user_id}\n")

    # Clear previous keys for clean test
    keys = r.keys(f"rate_limit:{user_id}:*")
    if keys:
        r.delete(*keys)

    # Simulate requests
    for i in range(1, 15):
        allowed = limiter.is_allowed(user_id)
        status = "Allowed" if allowed else "Blocked"
        print(f"Request {i}: {status}")
        
        # Sleep a bit to simulate real traffic, but mostly bursty here
        time.sleep(0.5) 
        
        # After 7 requests (approx 3.5s), we should have hit the limit of 5
        # The first 5 should be allowed. 6, 7 should be blocked.

    print("\nWaiting for window to expire...")
    time.sleep(window + 1)
    
    print("Sending another request...")
    allowed = limiter.is_allowed(user_id)
    status = "Allowed" if allowed else "Blocked"
    print(f"Request after window: {status}")

if __name__ == "__main__":
    main()
