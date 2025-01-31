import random
import time
from database.redis.collection_redis import CollectionRedisDao
from scraper.base_extractor import BaseExtractor
from config import BASE_URL, OUTPUT_FILE, MAX_PAGES, MIN_TIME_SLEEP_NEXT_BUTTON, \
    MAX_TIME_SLEEP_NEXT_BUTTON
from scraper.utils import save_json, clean_text, logger
from typing import Optional


class ReviewExtractor(BaseExtractor):
    def __init__(self):
        super().__init__()
        self.reviews = []
        self.redis_dao = CollectionRedisDao()
        self.min_time_sleep_next_button = MIN_TIME_SLEEP_NEXT_BUTTON
        self.max_time_sleep_next_button = MAX_TIME_SLEEP_NEXT_BUTTON

    def start_extract(self) -> None:
        """Start the extraction process"""
        logger.info("Starting the extraction process...")
        self.start_browser()
        self.navigate(BASE_URL)
        self.close_cookie_popup()

        for page_num in range(1, MAX_PAGES + 1):
            logger.info(f" Processing page {page_num}...")
            self.extract_reviews()
            self.click_next_button()

        self.close_browser()

        #  Save data
        save_json(OUTPUT_FILE, self.reviews)  # Save to reviews.json
        logger.info("Data extraction completed and saved.")

    def extract_reviews(self) -> None:
        """Extract reviews"""
        logger.info("Waiting for the reviews section to load...")
        self.page.wait_for_selector("section.styles_reviewsContainer__qcQUQ")
        reviews = self.page.query_selector_all("div.styles_reviewCardInner__UZk1x")

        for review in reviews:
            rating = self.extract_rating(review)
            text = review.query_selector("p.typography_body-l__v5JLj")
            review_text = text.inner_text() if text else "No text"

            date_element = review.query_selector("time")
            date = date_element.get_attribute("datetime") if date_element else None

            reviewer = self.extract_reviewer(review)
            replies = self._extract_replies(review)
            review_data = {
                "rating": rating,
                "text": clean_text(review_text),
                "date": date,
                "reviewer": reviewer,
                "replies": [clean_text(reply) for reply in replies]
            }

            # ⬅ Skip if the review is already processed
            if self.redis_dao.is_review_processed(review_text, date):
                logger.info(" This review has already been processed, skipping.")
                continue

            self.reviews.append(review_data)  # Store in main list

            self.redis_dao.save_review_to_redis(review_text, date, review_data)

            self.redis_dao.mark_review_as_processed(review_text, date)

    @staticmethod
    def _extract_replies(review):
        """Extracting reply responses"""
        replies = []

        reply_elements = review.query_selector_all(
            "p.typography_body-m__k2UI7.typography_appearance-default__t8iAq.styles_message____SVk")

        for reply in reply_elements:
            reply_text = reply.inner_text() if reply else "No reply text"
            replies.append(reply_text)

        return replies

    @staticmethod
    def extract_rating(review) -> Optional[int]:
        """Extract rating from the data-service-review-rating attribute"""
        rating_element = review.query_selector("div.styles_reviewHeader__xV2js")
        return int(rating_element.get_attribute("data-service-review-rating")) if rating_element else None

    @staticmethod
    def extract_reviewer(review) -> Optional[str]:
        """Extract reviewer name"""
        reviewer_element = review.query_selector("aside.styles_consumerInfoWrapper__MOCv1")
        if reviewer_element:
            reviewer_info = reviewer_element.get_attribute("aria-label")
            return reviewer_info.split("for")[1].strip() if reviewer_info else None
        return None

    def click_next_button(self) -> None:
        """Go to the next page"""
        try:
            next_button = self.page.query_selector("a.pagination-link_next__NdSsd")
            if next_button:
                next_button.scroll_into_view_if_needed()
                next_button.click()
                time.sleep(random.uniform(self.min_time_sleep_next_button, self.max_time_sleep_next_button))
                logger.info("Clicked the next button.")
            else:
                logger.info("No more pages to navigate.")
        except Exception as e:
            logger.error(f"Error clicking the next button: {e}")
