"""removed inherantance

Revision ID: 62f549df8c9e
Revises: 2dd47dce2a84
Create Date: 2022-06-07 15:14:18.364074

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62f549df8c9e'
down_revision = '2dd47dce2a84'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('files',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('userId', sa.Integer(), nullable=True),
    sa.Column('path', sa.String(), nullable=True),
    sa.Column('filename', sa.String(length=256), nullable=True),
    sa.Column('fileType', sa.String(length=5), nullable=True),
    sa.Column('courseCode', sa.String(length=16), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['userId'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_files_filename'), 'files', ['filename'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_files_filename'), table_name='files')
    op.drop_table('files')
    # ### end Alembic commands ###