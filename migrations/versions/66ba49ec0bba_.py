"""empty message

Revision ID: 66ba49ec0bba
Revises: 
Create Date: 2024-04-17 15:03:39.023475

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '66ba49ec0bba'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('addresses',
    sa.Column('address', sa.String(), nullable=False),
    sa.Column('latitude', sa.Float(), nullable=False),
    sa.Column('longitude', sa.Float(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False, comment='Идентификатор'),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, comment='Дата создания'),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, comment='Дата обновления'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_addresses_address'), 'addresses', ['address'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_addresses_address'), table_name='addresses')
    op.drop_table('addresses')
    # ### end Alembic commands ###
