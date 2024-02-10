"""create_initial_schema

Revision ID: cb5b5832ab95
Revises:
Create Date: 2023-03-28 03:30:04.921955+00:00

"""
import uuid

from alembic import op

import sqlalchemy as sa

from sqlalchemy.dialects.postgresql import UUID


revision = 'cb5b5832ab95'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'language_code',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=(sa.text("uuid_generate_v4()"))),
        sa.Column('code', sa.VARCHAR(2), nullable=False, unique=True),
        sa.Column('name', sa.Text, nullable=False, unique=True),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        'country_code',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=(sa.text("uuid_generate_v4()"))),
        sa.Column('code', sa.VARCHAR(2), nullable=False, unique=True),
        sa.Column('name', sa.Text, nullable=False, unique=True),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        'dataset',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=(sa.text("uuid_generate_v4()"))),
        sa.Column('name', sa.VARCHAR(64), nullable=False, unique=True),
        sa.Column('language_id', UUID(as_uuid=True), sa.ForeignKey('language_code.id'), nullable=False),
        sa.Column('translated', sa.Boolean, nullable=False),
        sa.Column('templated', sa.Boolean, nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        'task',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=(sa.text("uuid_generate_v4()"))),
        sa.Column('prompt', sa.Text, nullable=False, unique=True),
        sa.Column('completion', sa.Text, nullable=False, unique=True),
        sa.Column('task_type', sa.Enum('audit_translation', 'audit_xp3', name='task_type'), nullable=False),
        sa.Column('dataset_id', UUID(as_uuid=True), sa.ForeignKey('dataset.id'), nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        'user',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=(sa.text("uuid_generate_v4()"))),
        sa.Column('username', sa.VARCHAR(64), nullable=False, unique=True),
        sa.Column('image_url', sa.VARCHAR(256), nullable=False),
        sa.Column('country_code', UUID(as_uuid=True), sa.ForeignKey('country_code.id'), nullable=True),
        sa.Column('language_codes', sa.ARRAY(UUID(as_uuid=True)), nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        'task_submission',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=(sa.text("uuid_generate_v4()"))),
        sa.Column('task_id', UUID(as_uuid=True), sa.ForeignKey('task.id'), nullable=False),
        sa.Column('submitted_by', UUID(as_uuid=True), sa.ForeignKey('user.id'), nullable=False),
        sa.Column('submitted_prompt', sa.Text, nullable=False),
        sa.Column('submitted_completion', sa.Text, nullable=False),
        sa.Column('prompt_edited', sa.Boolean, nullable=False),
        sa.Column('completion_edited', sa.Boolean, nullable=False),
        sa.Column('prompt_rating', sa.Integer, nullable=True),
        sa.Column('completion_rating', sa.Integer, nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        'leaderboard_daily',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=(sa.text("uuid_generate_v4()"))),
        sa.Column('username', sa.VARCHAR(64), nullable=False),
        sa.Column('points', sa.Integer, nullable=False),
        sa.Column('day', sa.Date, nullable=False),
    )

    op.create_table(
        'leaderboard_weekly',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=(sa.text("uuid_generate_v4()"))),
        sa.Column('username', sa.VARCHAR(64), nullable=False),
        sa.Column('points', sa.Integer, nullable=False),
        sa.Column('week_of', sa.Date, nullable=False),
    )

    op.create_table(
        'leaderboard_by_language',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=(sa.text("uuid_generate_v4()"))),
        sa.Column('username', sa.VARCHAR(64), nullable=False),
        sa.Column('points', sa.Integer, nullable=False),
        sa.Column('language', sa.Text, nullable=False),
    )

    op.create_table(
        'leaderboard_overall',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=(sa.text("uuid_generate_v4()"))),
        sa.Column('username', sa.VARCHAR(64), nullable=False),
        sa.Column('points', sa.Integer, nullable=False),
    )



def downgrade() -> None:
    op.drop_table('leaderboard_daily')
    op.drop_table('leaderboard_weekly')
    op.drop_table('leaderboard_by_language')
    op.drop_table('leaderboard_overall')

    op.drop_table('task_submission')

    op.drop_table('user')
    op.drop_table('task')

    op.drop_table('country_code')
    op.drop_table('dataset')
    op.drop_table('language_code')

    op.execute('DROP TYPE task_type;')