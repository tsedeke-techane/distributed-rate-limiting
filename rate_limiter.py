import redis
import time

class FixedWindowRateLimiter:
    def __init__(self, redis_client: redis.Redis, limit: int, window_size_seconds: int = 60):
        """
        Initialize the FixedWindowRateLimiter.

        :param redis_client: The Redis client instance.
        :param limit: The maximum number of requests allowed in the window.
        :param window_size_seconds: The size of the time window in seconds (e.g., 60 for 1 minute).
        """
        self.redis = redis_client
        self.limit = limit
        self.window_size = window_size_seconds

    def is_allowed(self, user_id: str) -> bool:
        """
        Check if a request is allowed for the given user_id.

        :param user_id: The unique identifier for the user.
        :return: True if the request is allowed, False otherwise.
        """
        # Calculate the current window timestamp (e.g., current time // 60 for minute windows)
        current_window = int(time.time() // self.window_size)
        
        # Create a unique key for this user and window
        key = f"rate_limit:{user_id}:{current_window}"

        # Increment the counter for this key
        # Using a pipeline to ensure atomicity for the first increment + expire
        pipeline = self.redis.pipeline()
        pipeline.incr(key)
        pipeline.expire(key, self.window_size + 1) # Set expiry slightly longer than window
        results = pipeline.execute()

        request_count = results[0]

        if request_count > self.limit:
            return False
        
        return True
