"""Create user roles

Revision ID: 22de5b143d05
Revises: 9a8cc1906445
Create Date: 2025-01-06 13:40:11.307880

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column

# revision identifiers, used by Alembic.
revision = '22de5b143d05'
down_revision = '9a8cc1906445'
branch_labels = None
depends_on = None

roles_table = table('roles',
    column('id', sa.Integer),
    column('name', sa.String),
    column('description', sa.String)
)

def upgrade():
    roles = [
        {'name': 'super-admin', 'description': 'Super Admin, all admin perms and can create new admins'},
        {'name': 'admin', 'description': 'Can create/delete and modify bookings'},
        {'name': 'user', 'description': 'Standard user'}
    ]

    op.bulk_insert(roles_table, roles)

def downgrade():
    op.execute('DELETE FROM roles WHERE name IN ("super-admin", "admin", "user")')
