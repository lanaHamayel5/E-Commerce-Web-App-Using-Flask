"""rename column name

Revision ID: 3444d83a7726
Revises: 
Create Date: 2024-09-02 15:29:30.385019

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '3444d83a7726'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


from alembic import op
import sqlalchemy as sa

def upgrade() -> None:
    # Rename the column from 'category_id' to 'category_name'
    op.alter_column('product', 'category_id', new_column_name='category_name')
    
    # Update the foreign key constraint to reference 'category_name' in the 'category' table
    # op.drop_constraint('product_category_id_fkey', 'product', type_='foreignkey')
    # op.create_foreign_key(
    #     'product_category_name_fkey', 
    #     'product', 
    #     'category', 
    #     ['category_name'], 
    #     ['category_name']
    # )

def downgrade() -> None:
    # Rename the column from 'category_name' back to 'category_id'
    op.alter_column('product', 'category_name', new_column_name='category_id')
    
    # Restore the original foreign key constraint to reference 'category_id' in the 'category' table
    # op.drop_constraint('product_category_name_fkey', 'product', type_='foreignkey')
    # op.create_foreign_key(
    #     'product_category_id_fkey', 
    #     'product', 
    #     'category', 
    #     ['category_id'], 
    #     ['category_id']
    # )

