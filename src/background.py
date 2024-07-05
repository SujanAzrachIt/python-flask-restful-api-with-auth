import logging
from threading import Thread

import gevent
from flask import current_app

from .setting import AppSetting

logger = logging.getLogger(__name__)


class FlaskThread(Thread):
    """
    To make every new thread behinds Flask app context.
    Maybe using another lightweight solution but richer: APScheduler <https://github.com/agronholm/apscheduler>
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = current_app._get_current_object()

    def run(self):
        with self.app.app_context():
            super().run()


class Background:

    @staticmethod
    def run():
        setting: AppSetting = current_app.config[AppSetting.KEY]
        logger.info("Starting background...")

        # FlaskThread(target=Background.scrape_product, daemon=True).start()
        # FlaskThread(target=Background.update_product_details_periodically, daemon=True).start()
        Background.sync_on_start()

    # @staticmethod
    # def scrape_product():
    #     while True:
    #         from .services.scrapers.scraper import ScraperService
    #         ScraperService.scraping()
    #         gevent.sleep(10)
    #
    # @staticmethod
    # def update_product_details_periodically():
    #     while True:
    #         from .services.scrapers.scraper import ScraperService
    #         ScraperService.update_product_details()
    #         gevent.sleep(10)

    @staticmethod
    def sync_on_start():
        logger.info("Starting sync...")
