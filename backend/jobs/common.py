import logging

from collections import defaultdict

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
)


def even_out_ranks(records):
    """
    If any users have the same number of points, then they should have the same rank.
    """
    for i, record in enumerate(records):
        if i > 0:
            if record['points'] == records[i-1]['points']:
                record['rank'] = records[i-1]['rank']

    return records


def even_out_blended_ranks(records):
    """
    If any users have the same number of blended points, then they should
    have the same blended rank.
    """
    for i, record in enumerate(records):
        if i > 0:
            if record.blended_points == records[i-1].blended_points:
                record.blended_rank = records[i-1].blended_rank

    return records


def update_ranks_within_language_groups(records):
    """
    Group all the users together by the language (code) they have contributed to.

    Then, within each language group, re-rank the users based on the number of points
    they have earned in that language.
    """
    # group the records by language code
    language_groups = defaultdict(list)

    for record in records:
        language_code = record['language_code']

        if language_code in language_groups:
            language_groups[language_code].append(record)
        else:
            language_groups[language_code] = [record]

    # then re-rank the users within each language group
    updated_records = []
    for language_code, user_records in language_groups.items():
        # sort the records, which will be a list of dicts, by the number of points
        # each user has earned in that language (code)
        user_records.sort(key=lambda x: x['points'], reverse=True)

        # and then assign them a rank based on their position in the sorted list
        for i, record in enumerate(user_records):
                record['rank'] = i+1

        # if any users have the same number of points, then they should have
        # the same rank
        user_records = even_out_ranks(user_records)

        updated_records.extend(user_records)

    return updated_records


def update_blended_ranks_within_language_groups(records):
    """
    Group all the users together by the language (code) they have contributed to.

    Then, within each language group, re-rank the users based on the number of points
    they have earned in that language.
    """
    # group the records by language code
    language_groups = defaultdict(list)

    for record in records:
        language_code = record.language_code

        if language_code in language_groups:
            language_groups[language_code].append(record)
        else:
            language_groups[language_code] = [record]

    # then re-rank the users within each language group
    updated_records = []
    for language_code, user_records in language_groups.items():
        # sort the records, which will be a list of dicts, by the number of points
        # each user has earned in that language (code)
        user_records.sort(key=lambda x: x.blended_points, reverse=True)

        # and then assign them a rank based on their position in the sorted list
        for i, record in enumerate(user_records):
            record.blended_rank = i+1

        # if any users have the same number of points, then they should have
        # the same rank
        user_records = even_out_blended_ranks(user_records)

        updated_records.extend(user_records)

    return updated_records


def compute_aya_score(
    avg_quality_score,
    num_audits_edited,
    num_audits_further_improved,
    thumbs_up_received_ratio,
    num_contributed_tasks,
):
    logger.debug(
        f'Aya score params: '
        f'{max(0, (avg_quality_score - 3))} *'
        f'({num_audits_edited} + {num_audits_further_improved}) +'
        f'({thumbs_up_received_ratio} * {num_contributed_tasks})'
    )
    score = (
        max(0, (avg_quality_score - 3)) *
        (num_audits_edited + num_audits_further_improved) +
        (thumbs_up_received_ratio * num_contributed_tasks)
    )
    logger.debug(f'results: {score}')
    return score