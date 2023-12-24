"""add password reset token table

Revision ID: 2b40e5688c2f
Revises: 
Create Date: 2023-12-24 21:44:04.826814

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2b40e5688c2f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("password_reset_tokens",
                    sa.Column("id", sa.Integer,
                              primary_key=True, nullable=False),
                    sa.Column("otp", sa.String(), nullable=False),
                    sa.Column("user_email", sa.String(),
                              nullable=False, unique=True, index=True),
                    sa.Column("expiry_time", sa.TIMESTAMP, nullable=False, server_default=sa.text(
                        'NOW() + INTERVAL \'5 minutes\'')),
                    )


def downgrade() -> None:
    op.drop_table("password_reset_tokens")
