"""empty message

Revision ID: ee543d5d75a3
Revises: 
Create Date: 2024-01-07 20:02:09.238728

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ee543d5d75a3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('healthconditions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('treatment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('condition', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password_hash', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('chat',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_chat_user_id_users')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('healthcondition_treatment_association',
    sa.Column('healthcondition_id', sa.Integer(), nullable=True),
    sa.Column('treatment_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['healthcondition_id'], ['healthconditions.id'], name=op.f('fk_healthcondition_treatment_association_healthcondition_id_healthconditions')),
    sa.ForeignKeyConstraint(['treatment_id'], ['treatment.id'], name=op.f('fk_healthcondition_treatment_association_treatment_id_treatment'))
    )
    op.create_table('chat_healthconditions_association',
    sa.Column('chat_id', sa.Integer(), nullable=True),
    sa.Column('healthcondition_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['chat_id'], ['chat.id'], name=op.f('fk_chat_healthconditions_association_chat_id_chat')),
    sa.ForeignKeyConstraint(['healthcondition_id'], ['healthconditions.id'], name=op.f('fk_chat_healthconditions_association_healthcondition_id_healthconditions'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('chat_healthconditions_association')
    op.drop_table('healthcondition_treatment_association')
    op.drop_table('chat')
    op.drop_table('users')
    op.drop_table('treatment')
    op.drop_table('healthconditions')
    # ### end Alembic commands ###
