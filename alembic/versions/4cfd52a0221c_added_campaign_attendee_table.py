"""added campaign attendee table

Revision ID: 4cfd52a0221c
Revises: 7ec6bb5b1275
Create Date: 2024-02-05 15:39:38.078093

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4cfd52a0221c'
down_revision: Union[str, None] = '7ec6bb5b1275'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('campaign_attendees',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('donor_id', sa.Integer(), nullable=True),
                    sa.Column('campaign_id', sa.Integer(), nullable=True),
                    sa.Column('donated', sa.Boolean(), nullable=True),
                    sa.ForeignKeyConstraint(
                        ['campaign_id'], ['campaigns.id'], ),
                    sa.ForeignKeyConstraint(['donor_id'], ['donors.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_campaign_attendees_id'),
                    'campaign_attendees', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_campaign_attendees_id'),
                  table_name='campaign_attendees')
    op.drop_table('campaign_attendees')
    # ### end Alembic commands ###
