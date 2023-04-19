"""Add icon_color table

Revision ID: c105ae36dcd5
Revises: 66a46905b1df
Create Date: 2023-04-18 11:26:30.737097

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c105ae36dcd5"
down_revision = "66a46905b1df"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "colors",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
    )
    op.create_index(op.f("ix_colors_id"), "colors", ["id"], unique=False)
    op.create_table(
        "icons",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("url", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("url"),
    )
    op.create_index(op.f("ix_icons_id"), "icons", ["id"], unique=False)
    op.create_table(
        "icon_color",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("color_id", sa.Integer(), nullable=False),
        sa.Column("icon_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["color_id"],
            ["colors.id"],
        ),
        sa.ForeignKeyConstraint(
            ["icon_id"],
            ["icons.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_icon_color_id"), "icon_color", ["id"], unique=False)
    op.add_column("groups", sa.Column("icon_color_id", sa.Integer(), nullable=False))
    op.create_foreign_key(None, "groups", "icon_color", ["icon_color_id"], ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "groups", type_="foreignkey")
    op.drop_column("groups", "icon_color_id")
    op.drop_index(op.f("ix_icon_color_id"), table_name="icon_color")
    op.drop_table("icon_color")
    op.drop_index(op.f("ix_icons_id"), table_name="icons")
    op.drop_table("icons")
    op.drop_index(op.f("ix_colors_id"), table_name="colors")
    op.drop_table("colors")
    # ### end Alembic commands ###
