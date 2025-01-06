"""Add fs_uniquifier field to User model

Revision ID: 9a8cc1906445
Revises: 68d89ef13132
Create Date: 2025-01-06 12:52:57.272220

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql
import os

# revision identifiers, used by Alembic.
revision = '9a8cc1906445'
down_revision = '68d89ef13132'
branch_labels = None
depends_on = None

def column_exists(table_name, column_name):
    inspector = sa.inspect(op.get_bind())
    return column_name in [col['name'] for col in inspector.get_columns(table_name)]

def index_exists(table_name, index_name):
    inspector = sa.inspect(op.get_bind())
    indexes = inspector.get_indexes(table_name)
    return any(index['name'] == index_name for index in indexes)

def upgrade():
    # Conditionally create roles table
    if not op.get_bind().dialect.has_table(op.get_bind(), "roles"):
        op.create_table('roles',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('name', sa.String(length=80), nullable=True),
            sa.Column('description', sa.String(length=255), nullable=True),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('name')
        )
    
    # Conditionally create roles_users table
    if not op.get_bind().dialect.has_table(op.get_bind(), "roles_users"):
        op.create_table('roles_users',
            sa.Column('user_id', sa.Integer(), nullable=True),
            sa.Column('role_id', sa.Integer(), nullable=True),
            sa.ForeignKeyConstraint(['role_id'], ['roles.id']),
            sa.ForeignKeyConstraint(['user_id'], ['users.id'])
        )
    
    with op.batch_alter_table('listing_images', schema=None) as batch_op:
        batch_op.alter_column('main_image',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.SmallInteger(),
               existing_nullable=False,
               existing_server_default=sa.text("'0'"))

    # Assign unique values to fs_uniquifier for existing users before adding the unique constraint
    conn = op.get_bind()
    users = conn.execute(sa.text("SELECT id FROM users WHERE fs_uniquifier IS NULL OR fs_uniquifier = ''")).fetchall()
    for user in users:
        conn.execute(sa.text("UPDATE users SET fs_uniquifier = :fs_uniquifier WHERE id = :id"), {'fs_uniquifier': os.urandom(32).hex(), 'id': user.id})

    with op.batch_alter_table('users', schema=None) as batch_op:
        if index_exists('users', 'api_token'):
            batch_op.drop_index('api_token')
        batch_op.create_unique_constraint(None, ['fs_uniquifier'])
        if column_exists('users', 'token_expiry'):
            batch_op.drop_column('token_expiry')
        if column_exists('users', 'api_token'):
            batch_op.drop_column('api_token')
        if column_exists('users', 'role_id'):
            batch_op.drop_column('role_id')

def downgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('role_id', mysql.SMALLINT(), server_default=sa.text("'1'"), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('api_token', mysql.VARCHAR(length=255), nullable=True))
        batch_op.add_column(sa.Column('token_expiry', mysql.DATETIME(), nullable=True))
        batch_op.drop_constraint(None, type_='unique')
        batch_op.create_index('api_token', ['api_token'], unique=True)
        batch_op.drop_column('fs_uniquifier')

    with op.batch_alter_table('listing_images', schema=None) as batch_op:
        batch_op.alter_column('main_image',
               existing_type=sa.SmallInteger(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=False,
               existing_server_default=sa.text("'0'"))

    op.drop_table('roles_users')
    op.drop_table('roles')
