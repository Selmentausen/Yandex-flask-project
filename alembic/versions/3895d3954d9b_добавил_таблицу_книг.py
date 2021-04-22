"""добавил таблицу книг

Revision ID: 3895d3954d9b
Revises: 
Create Date: 2021-04-22 16:46:14.975139

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3895d3954d9b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('books',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('author', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('content', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_books_content'), 'books', ['content'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_books_content'), table_name='books')
    op.drop_table('books')
    # ### end Alembic commands ###
