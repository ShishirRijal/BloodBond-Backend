"""add campaign table

Revision ID: a42f97f765b5
Revises: 5658ecdf5822
Create Date: 2024-02-02 21:13:37.915056

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a42f97f765b5'
down_revision: Union[str, None] = '5658ecdf5822'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('campaigns',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('address', sa.String(), nullable=False),
    sa.Column('city', sa.String(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('banner', sa.String(), nullable=False),
    sa.Column('interested_donors', sa.Integer(), nullable=False),
    sa.Column('donated_donors', sa.Integer(), nullable=False),
    sa.Column('total_bags', sa.Integer(), nullable=False),
    sa.Column('hospital_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['hospital_id'], ['hospitals.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_campaigns_city'), 'campaigns', ['city'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_campaigns_city'), table_name='campaigns')
    op.drop_table('campaigns')
    # ### end Alembic commands ###
