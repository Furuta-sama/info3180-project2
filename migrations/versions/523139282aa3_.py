"""empty message

Revision ID: 523139282aa3
Revises: e402e5714ebe
Create Date: 2021-04-24 02:22:02.179617

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '523139282aa3'
down_revision = 'e402e5714ebe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Favourites',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('car_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cars',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.Integer(), nullable=True),
    sa.Column('make', sa.String(length=250), nullable=True),
    sa.Column('model', sa.String(length=300), nullable=True),
    sa.Column('colour', sa.DateTime(), nullable=True),
    sa.Column('year', sa.String(length=50), nullable=True),
    sa.Column('transmission', sa.String(length=300), nullable=True),
    sa.Column('car_type', sa.String(length=300), nullable=True),
    sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.Column('photo', sa.String(length=300), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('make')
    )
    op.drop_table('follows')
    op.drop_table('likes')
    op.drop_table('posts')
    op.add_column('users', sa.Column('date_joined', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('name', sa.String(length=300), nullable=True))
    op.add_column('users', sa.Column('photo', sa.String(length=250), nullable=True))
    op.drop_column('users', 'firstname')
    op.drop_column('users', 'lastname')
    op.drop_column('users', 'profile_photo')
    op.drop_column('users', 'joined_on')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('joined_on', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column('users', sa.Column('profile_photo', sa.VARCHAR(length=250), autoincrement=False, nullable=True))
    op.add_column('users', sa.Column('lastname', sa.VARCHAR(length=80), autoincrement=False, nullable=True))
    op.add_column('users', sa.Column('firstname', sa.VARCHAR(length=80), autoincrement=False, nullable=True))
    op.drop_column('users', 'photo')
    op.drop_column('users', 'name')
    op.drop_column('users', 'date_joined')
    op.create_table('posts',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('photo', sa.VARCHAR(length=250), autoincrement=False, nullable=True),
    sa.Column('caption', sa.VARCHAR(length=300), autoincrement=False, nullable=True),
    sa.Column('created_on', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='posts_pkey'),
    sa.UniqueConstraint('photo', name='posts_photo_key')
    )
    op.create_table('likes',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('post_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='likes_pkey')
    )
    op.create_table('follows',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('follower_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='follows_pkey')
    )
    op.drop_table('cars')
    op.drop_table('Favourites')
    # ### end Alembic commands ###