"""empty message

Revision ID: 2c32abc9392a
Revises: 
Create Date: 2021-07-07 20:07:13.374865

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2c32abc9392a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ner_tag_type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('short_name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_ner_tag_type'))
    )
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_role')),
    sa.UniqueConstraint('name', name=op.f('uq_role_name'))
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('password', sa.String(length=255), server_default='', nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('confirmed_at', sa.DateTime(), nullable=True),
    sa.Column('is_active', sa.Boolean(), server_default='0', nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_user')),
    sa.UniqueConstraint('email', name=op.f('uq_user_email')),
    sa.UniqueConstraint('username', name=op.f('uq_user_username'))
    )
    op.create_table('files',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_files_user_id_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_files'))
    )
    op.create_table('profiles',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('first_name', sa.String(length=64), nullable=False),
    sa.Column('last_name', sa.String(length=64), nullable=False),
    sa.Column('date_of_birth', sa.DATE(), nullable=False),
    sa.Column('img_url', sa.String(), nullable=True),
    sa.Column('comp_name', sa.String(length=64), nullable=True),
    sa.Column('web_page', sa.String(length=64), nullable=True),
    sa.Column('info', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_profiles_user_id_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_profiles'))
    )
    op.create_table('user_roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], name=op.f('fk_user_roles_role_id_role'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_user_roles_user_id_user'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_user_roles'))
    )
    op.create_table('pages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('file_id', sa.Integer(), nullable=True),
    sa.Column('start_index', sa.Integer(), nullable=True),
    sa.Column('end_index', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['file_id'], ['files.id'], name=op.f('fk_pages_file_id_files')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_pages'))
    )
    op.create_table('statistics',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('file_id', sa.Integer(), nullable=True),
    sa.Column('words', sa.Integer(), nullable=True),
    sa.Column('uniq_words', sa.Integer(), nullable=True),
    sa.Column('sentences', sa.Integer(), nullable=True),
    sa.Column('avg_words_in_sentence', sa.Integer(), nullable=True),
    sa.Column('avg_chars_in_sentence', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['file_id'], ['files.id'], name=op.f('fk_statistics_file_id_files')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_statistics'))
    )
    op.create_table('status',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('file_id', sa.Integer(), nullable=True),
    sa.Column('lemmatized', sa.Boolean(), nullable=True),
    sa.Column('tokenized', sa.Boolean(), nullable=True),
    sa.Column('pos_tagged', sa.Boolean(), nullable=True),
    sa.Column('stop_words_removed', sa.Boolean(), nullable=True),
    sa.Column('frequency_distribution_calculated', sa.Boolean(), nullable=True),
    sa.Column('completed', sa.Boolean(), nullable=True),
    sa.Column('punctuation_removed', sa.Boolean(), nullable=True),
    sa.Column('cleared_html_tags', sa.Boolean(), nullable=True),
    sa.Column('special_chars_removed', sa.Boolean(), nullable=True),
    sa.Column('cleared_whitespaces', sa.Boolean(), nullable=True),
    sa.Column('html_tags_removed', sa.Boolean(), nullable=True),
    sa.Column('expanded_acronyms', sa.Boolean(), nullable=True),
    sa.Column('words_enumerated', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['file_id'], ['files.id'], name=op.f('fk_status_file_id_files')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_status'))
    )
    op.create_table('ner_tags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('page_id', sa.Integer(), nullable=True),
    sa.Column('ner_tag_type_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['ner_tag_type_id'], ['ner_tag_type.id'], name=op.f('fk_ner_tags_ner_tag_type_id_ner_tag_type')),
    sa.ForeignKeyConstraint(['page_id'], ['pages.id'], name=op.f('fk_ner_tags_page_id_pages')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_ner_tags'))
    )
    op.create_table('sentences',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('page_id', sa.Integer(), nullable=True),
    sa.Column('start_index', sa.Integer(), nullable=True),
    sa.Column('end_index', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['page_id'], ['pages.id'], name=op.f('fk_sentences_page_id_pages')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_sentences'))
    )
    op.create_table('words',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sentence_id', sa.Integer(), nullable=True),
    sa.Column('start_index', sa.Integer(), nullable=True),
    sa.Column('end_index', sa.Integer(), nullable=True),
    sa.Column('raw', sa.String(), nullable=True),
    sa.Column('lemma', sa.String(), nullable=True),
    sa.Column('pos_tags', sa.String(), nullable=True),
    sa.Column('ner_tags_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['ner_tags_id'], ['ner_tags.id'], name=op.f('fk_words_ner_tags_id_ner_tags')),
    sa.ForeignKeyConstraint(['sentence_id'], ['sentences.id'], name=op.f('fk_words_sentence_id_sentences')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_words'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('words')
    op.drop_table('sentences')
    op.drop_table('ner_tags')
    op.drop_table('status')
    op.drop_table('statistics')
    op.drop_table('pages')
    op.drop_table('user_roles')
    op.drop_table('profiles')
    op.drop_table('files')
    op.drop_table('user')
    op.drop_table('role')
    op.drop_table('ner_tag_type')
    # ### end Alembic commands ###
