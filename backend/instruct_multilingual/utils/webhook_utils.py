import logging
import time

from typing import List, Optional

import requests

from instruct_multilingual.config import get_settings

settings = get_settings()

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
)

# normally, we'd want to do this async, but
# instead we'll use a background task since the
# API layer is not async
def send_discord_webhook_message(message: str, embeds: Optional[List[str]] = None):
    """
    Sends a message to a discord webhook.
    """
    # bail out if the webhook URL is not set
    if not settings.discord_webhook_url or settings.discord_webhook_url is None:
        logger.info(
            f"discord webhook URL not set, skipping webhook payload delivery"
        )
        return

    # send a message to a discord webhook
    # and use the default username and avatar
    data = {"content" : message}

    if embeds is not None:
        data["embeds"] = embeds

    logger.info(f"sending discord webhook payload...")

    # time the request
    start_time = time.time()

    response = requests.post(
        settings.discord_webhook_url,
        json=data,
    )

    elapsed_time = time.time() - start_time

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        logger.error(err)
    else:
        logger.info(
            f"payload took {elapsed_time:.2f} seconds with status code {response.status_code}"
        )
    