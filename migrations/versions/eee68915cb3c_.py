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


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.Column('first_name', sa.String(), nullable=False),
                    sa.Column('last_name', sa.String(), nullable=True),
                    sa.Column('email', sa.String(), nullable=True),
                    sa.Column('password', sa.String(), nullable=True),
                    sa.Column('date_created', sa.DateTime(), nullable=True),
                    sa.PrimaryKeyConstraint('user_id')
                    )

    op.create_table('docking_jobs',
                    sa.Column('docking_id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.Column('job_status_id', sa.Integer(), nullable=True),
                    sa.Column('date_started', sa.DateTime(), nullable=True),
                    sa.PrimaryKeyConstraint('docking_id')
                    )

    op.create_table('job_status',
                    sa.Column('job_status_id', sa.Integer(), nullable=False),
                    sa.Column('job_status_name', sa.String(length=64), nullable=True),
                    sa.PrimaryKeyConstraint('job_status_id')
                    )


    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('job_status')
    op.drop_table('docking_jobs')
    # ### end Alembic commands ###
