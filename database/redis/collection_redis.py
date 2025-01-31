from config import REDIS_SERVER_IP, REDIS_SERVER_PORT
from database.redis.base_redis import BaseRedisDao
import json


class CollectionRedisDao(BaseRedisDao):
    def __init__(self):
        super().__init__(host=REDIS_SERVER_IP, port=REDIS_SERVER_PORT)

    def is_review_processed(self, review_text: str, date: str) -> bool:
        """Check if the review has already been processed"""
        review_key = f"{review_text.strip()}_{date}"
        connection = self.get_connection()
        return connection.sismember("visited_reviews", review_key)

    def mark_review_as_processed(self, review_text: str, date: str) -> None:
        """Mark the review as processed in Redis"""
        review_key = f"{review_text.strip()}_{date}"
        connection = self.get_connection()
        connection.sadd("visited_reviews", review_key)

    def save_review_to_redis(self, review_text, date, review_data) -> None:
        """Save the review data to Redis"""
        review_key = f"{review_text.strip()}_{date}"
        connection = self.get_connection()

        # Serialize any list values in review_data to JSON
        for key, value in review_data.items():
            if isinstance(value, list):  # Check if the value is a list
                review_data[key] = json.dumps(value)  # Convert list to a JSON string

        # Save data as a hash
        connection.hset(review_key, mapping=review_data)
