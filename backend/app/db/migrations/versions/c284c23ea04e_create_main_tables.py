"""create_main_tables
Revision ID: c284c23ea04e
Revises: 
Create Date: 2021-07-27 19:14:46.461903
"""
from sqlalchemy.sql.schema import Column, ForeignKey
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic
revision = 'c284c23ea04e'
down_revision = None
branch_labels = None
depends_on = None

def table_cleaning() -> None: 
    op.create_table( #Se llama el objeto de alembic para crear la tabla
        'cleaning', #Nombre de la tabla
        sa.Column("id",             sa.Integer,             primary_key=True                                    ),
        sa.Column("name",           sa.Text,                nullable=False,     index=True                      ),
        sa.Column("description",    sa.Text,                nullable=True                                       ),
        sa.Column("cleaning_type",  sa.Text,                nullable=False,     server_default="spot_clean"     ),
        sa.Column("price",          sa.Numeric(10, 2),      nullable=False                                      )
    )

#Nullable es que el valor puede ser nulo
def upgrade() -> None:
    table_cleaning()
    
def downgrade() -> None:
    op.drop_table('cleaning')

#The two main functions - upgrade and downgrade - will be used to create and drop database tables, execute SQL commands, and each time we migrate