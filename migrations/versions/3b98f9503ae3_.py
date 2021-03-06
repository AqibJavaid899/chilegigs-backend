"""empty message

Revision ID: 3b98f9503ae3
Revises: 
Create Date: 2020-12-15 22:41:10.380587

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b98f9503ae3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('objetosglobales',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('requisitos', sa.Text(), nullable=True),
    sa.Column('home', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('account',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('username', sa.String(length=100), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('password', sa.String(length=100), nullable=True),
    sa.Column('time_created', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('clientprofile',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('client_id', sa.Integer(), nullable=True),
    sa.Column('status', sa.String(length=50), nullable=True),
    sa.Column('nombre', sa.String(length=100), nullable=True),
    sa.Column('apellido', sa.String(length=100), nullable=True),
    sa.Column('imagen', sa.String(length=300), nullable=True),
    sa.Column('rut', sa.String(length=100), nullable=True),
    sa.Column('nacionalidad', sa.String(length=100), nullable=True),
    sa.Column('ciudad', sa.String(length=100), nullable=True),
    sa.Column('pais', sa.String(length=100), nullable=True),
    sa.Column('biografia', sa.String(length=100), nullable=True),
    sa.Column('suma_rating', sa.Integer(), nullable=True),
    sa.Column('contrataciones', sa.Integer(), nullable=True),
    sa.Column('feedback', sa.String(length=1000), nullable=True),
    sa.ForeignKeyConstraint(['client_id'], ['account.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('djprofile',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('dj_id', sa.Integer(), nullable=True),
    sa.Column('artista', sa.String(length=100), nullable=True),
    sa.Column('ciudad', sa.String(length=100), nullable=True),
    sa.Column('username', sa.String(length=100), nullable=True),
    sa.Column('pais', sa.String(length=100), nullable=True),
    sa.Column('imagen', sa.String(length=300), nullable=True),
    sa.Column('status', sa.String(length=50), nullable=True),
    sa.Column('mixcloud', sa.String(length=100), nullable=True),
    sa.Column('soundcloud', sa.String(length=100), nullable=True),
    sa.Column('instagram', sa.String(length=100), nullable=True),
    sa.Column('generos', sa.String(length=500), nullable=True),
    sa.Column('servicios', sa.String(length=500), nullable=True),
    sa.Column('tecnica', sa.String(length=500), nullable=True),
    sa.Column('agregar_cancion', sa.Boolean(), server_default=sa.text('false'), nullable=True),
    sa.Column('url_cancion', sa.String(length=100), nullable=True),
    sa.Column('biografia', sa.String(length=1000), nullable=True),
    sa.Column('dur_min', sa.String(length=10), nullable=True),
    sa.Column('dur_max', sa.String(length=10), nullable=True),
    sa.Column('viajes', sa.String(length=10), nullable=True),
    sa.Column('staff', sa.Integer(), nullable=True),
    sa.Column('arrienda_equipos', sa.String(length=10), nullable=True),
    sa.Column('requisitos', sa.String(length=1000), nullable=True),
    sa.Column('datos', sa.String(length=1000), nullable=True),
    sa.Column('suma_rating', sa.Integer(), nullable=True),
    sa.Column('contrataciones', sa.Integer(), nullable=True),
    sa.Column('feedback', sa.String(length=1000), nullable=True),
    sa.ForeignKeyConstraint(['dj_id'], ['account.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('gig',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('client_id', sa.Integer(), nullable=True),
    sa.Column('dj_id', sa.Integer(), nullable=True),
    sa.Column('estado', sa.String(length=100), nullable=True),
    sa.Column('username_cliente', sa.String(length=100), nullable=True),
    sa.Column('username_dj', sa.String(length=100), nullable=True),
    sa.Column('dia_evento', sa.String(length=100), nullable=True),
    sa.Column('tipo_evento', sa.String(length=100), nullable=True),
    sa.Column('nombre_evento', sa.String(length=100), nullable=True),
    sa.Column('telefono', sa.String(length=100), nullable=True),
    sa.Column('direccion', sa.String(length=100), nullable=True),
    sa.Column('duracion', sa.String(length=100), nullable=True),
    sa.Column('hora_llegada', sa.String(length=100), nullable=True),
    sa.Column('hora_show', sa.String(length=100), nullable=True),
    sa.Column('transporte', sa.String(length=100), nullable=True),
    sa.Column('oferta', sa.String(length=100), nullable=True),
    sa.Column('link_evento', sa.String(length=100), nullable=True),
    sa.Column('privado', sa.Boolean(), server_default=sa.text('false'), nullable=True),
    sa.Column('leido_por_dj', sa.Boolean(), server_default=sa.text('false'), nullable=True),
    sa.Column('leido_por_cliente', sa.Boolean(), server_default=sa.text('false'), nullable=True),
    sa.Column('mensaje', sa.String(length=10000), nullable=True),
    sa.Column('time_created', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['client_id'], ['account.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['dj_id'], ['account.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('gig')
    op.drop_table('djprofile')
    op.drop_table('clientprofile')
    op.drop_table('account')
    op.drop_table('roles')
    op.drop_table('objetosglobales')
    # ### end Alembic commands ###
