"""initial_schema

Revision ID: 001
Revises: 
Create Date: 2026-06-27 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('jobs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('source_id', sa.String(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('company', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('url', sa.String(), nullable=True),
        sa.Column('location', sa.String(), nullable=True),
        sa.Column('country', sa.String(), nullable=True),
        sa.Column('employment_type', sa.String(), nullable=True),
        sa.Column('experience_level', sa.String(), nullable=True),
        sa.Column('salary_min', sa.Numeric(), nullable=True),
        sa.Column('salary_max', sa.Numeric(), nullable=True),
        sa.Column('currency', sa.String(length=3), nullable=True),
        sa.Column('meta_source', sa.String(), nullable=False),
        sa.Column('meta_pipeline_version', sa.String(), nullable=False),
        sa.Column('meta_first_seen_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('meta_last_seen_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('meta_processing_duration', sa.Numeric(), nullable=True),
        sa.Column('fingerprint', sa.String(), nullable=False),
        sa.Column('skills', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('raw_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_jobs_company'), 'jobs', ['company'], unique=False)
    op.create_index(op.f('ix_jobs_fingerprint'), 'jobs', ['fingerprint'], unique=True)
    op.create_index(op.f('ix_jobs_id'), 'jobs', ['id'], unique=False)
    op.create_index(op.f('ix_jobs_meta_source'), 'jobs', ['meta_source'], unique=False)
    op.create_index(op.f('ix_jobs_source_id'), 'jobs', ['source_id'], unique=False)
    op.create_index(op.f('ix_jobs_title'), 'jobs', ['title'], unique=False)

def downgrade():
    op.drop_index(op.f('ix_jobs_title'), table_name='jobs')
    op.drop_index(op.f('ix_jobs_source_id'), table_name='jobs')
    op.drop_index(op.f('ix_jobs_meta_source'), table_name='jobs')
    op.drop_index(op.f('ix_jobs_id'), table_name='jobs')
    op.drop_index(op.f('ix_jobs_fingerprint'), table_name='jobs')
    op.drop_index(op.f('ix_jobs_company'), table_name='jobs')
    op.drop_table('jobs')
