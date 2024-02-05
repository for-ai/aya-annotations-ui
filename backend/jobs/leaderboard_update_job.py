import click
import logging

from collections import defaultdict
from datetime import datetime, timedelta

from sqlalchemy import text
from sqlalchemy.dialects.postgresql import insert

from sqlmodel import Session

from instruct_multilingual import db

from jobs import (
    update_leaderboard_by_language,
    update_leaderboard_daily,
    update_leaderboard_overall,
    update_leaderboard_weekly,
)


logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
)


@click.command()
@click.option(
    '--leaderboard',
    '-l',
    type=click.Choice([
        'daily',
        'weekly',
        'by_language',
        'overall',
    ]),
    required=True,
)
def update_leaderboard(leaderboard):
    """
    Update the leaderboard specified by the argument.
    """
    if leaderboard == 'daily':
        update_leaderboard_daily()
    elif leaderboard == 'weekly':
        update_leaderboard_weekly()
    elif leaderboard == 'by_language':
        update_leaderboard_by_language()
    elif leaderboard == 'overall':
        update_leaderboard_overall()


if __name__ == '__main__':
    update_leaderboard()
