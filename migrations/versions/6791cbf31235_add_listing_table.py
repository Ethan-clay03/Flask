"""Add listing table

Revision ID: 6791cbf31235
Revises: ac9d4555724d
Create Date: 2024-11-05 10:36:32.872815

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector


# revision identifiers, used by Alembic.
revision = '6791cbf31235'
down_revision = 'ac9d4555724d'
branch_labels = None
depends_on = None


def upgrade():
       bind = op.get_bind()
       inspector = Inspector.from_engine(bind)

       # Check if the 'users' table exists
       if 'listings' not in inspector.get_table_names():
              op.create_table(
                     'listings',
                     sa.Column('id', sa.Integer(), nullable=False, autoincrement=True, primary_key=True),
                     sa.Column('depart_location', sa.String(255), nullable=False),
                     sa.Column('depart_time', sa.DateTime(), nullable=False),
                     sa.Column('destination_location', sa.String(255), nullable=False),
                     sa.Column('destination_time', sa.DateTime(), nullable=False),
                     sa.Column('fair_cost', sa.Float(2), nullable=False),
                     sa.Column('transport_type', sa.String(255), nullable=False),
                     sa.Column('business_tickets', sa.Integer(), nullable=False),
                     sa.Column('economy_tickets', sa.Integer(), nullable=False)
              )