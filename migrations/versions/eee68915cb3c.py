"""empty message

Revision ID: eee68915cb3c
Revises: 
Create Date: 2018-02-11 19:10:09.737630

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'eee68915cb3c'
down_revision = None
branch_labels = None
depends_on = None

def insert_job_status_data():
    job_status_table = sa.sql.table('job_status', sa.sql.column('job_status_id'), sa.sql.column('job_status_name'))
    op.bulk_insert(job_status_table,
                   [
                       {'job_status_id': 1, 'job_status_name': 'Completed'},
                       {'job_status_id': 2, 'job_status_name': 'Failed'},
                       {'job_status_id': 3, 'job_status_name': 'Submitted'},
                       {'job_status_id': 4, 'job_status_name': 'Partial results available'},
                       {'job_status_id': 5, 'job_status_name': 'Upload in progress'},
                       {'job_status_id': 6, 'job_status_name': 'Running'},
                       {'job_status_id': 7, 'job_status_name': 'Terminated by user'},
                       {'job_status_id': 8, 'job_status_name': 'Terminated by system'},
                       {'job_status_id': 9, 'job_status_name': 'Awaiting user response'},
                   ], multiinsert=False
                   )


def insert_job_types_data():
    job_types_table = sa.sql.table('job_types', sa.sql.column('job_type_id'),
                                                              sa.sql.column('short_name'), sa.sql.column('long_name'))
    op.bulk_insert(job_types_table,
                   [
                       {'job_type_id': 1, 'short_name': 'cluster', 'long_name': 'Cluster'},
                       {'job_type_id': 2, 'short_name': 'dock', 'long_name': 'Dock'},
                       {'job_type_id': 3, 'short_name': 'prepare', 'long_name': 'Prepare'},
                       {'job_type_id': 4, 'short_name': 'calibrate', 'long_name': 'Calibrate'},
                       {'job_type_id': 5, 'short_name': 'decoys', 'long_name': 'Decoys'},
                       {'job_type_id': 6, 'short_name': 'build2d', 'long_name': 'Build 2D'},
                       {'job_type_id': 7, 'short_name': 'build3d', 'long_name': 'Build 3D'}
                   ], multiinsert=False
                   )


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('first_name', sa.String(), nullable=False),
                    sa.Column('last_name', sa.String(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('date_created', sa.DateTime(), nullable=False),
                    sa.Column('admin', sa.Boolean, nullable=False),
                    sa.Column('deleted', sa.Boolean, nullable=False),
                    sa.Column('api_key', sa.String(), nullable=False),
                    sa.PrimaryKeyConstraint('user_id'),
                    sa.UniqueConstraint('email'),
                    sa.UniqueConstraint('api_key')
                    )

    op.create_table('docking_jobs',
                    sa.Column('docking_job_id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('job_status_id', sa.Integer(), nullable=False),
                    sa.Column('last_updated', sa.DateTime(), nullable=False),
                    sa.Column('job_type_id', sa.Integer(), nullable=False),
                    sa.Column('memo', sa.String(), nullable=False),
                    sa.Column('marked_favorite', sa.Integer(), nullable=False),
                    sa.Column('deleted', sa.Boolean(), nullable=False),
                    sa.PrimaryKeyConstraint('docking_job_id')
                    )

    op.create_table('job_status',
                    sa.Column('job_status_id', sa.Integer(), nullable=False),
                    sa.Column('job_status_name', sa.String(length=64), nullable=False),
                    sa.PrimaryKeyConstraint('job_status_id')
                    )
    insert_job_status_data()

    op.create_table('job_types',
                    sa.Column('job_type_id', sa.Integer(), nullable=False),
                    sa.Column('short_name', sa.String(), nullable=False),
                    sa.Column('long_name', sa.String(), nullable=False)
                    )
    insert_job_types_data()
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('job_status')
    op.drop_table('docking_jobs')
    op.drop_table('job_types')
    # ### end Alembic commands ###
