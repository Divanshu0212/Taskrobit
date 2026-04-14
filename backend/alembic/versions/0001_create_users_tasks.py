"""create users and tasks tables"""

from alembic import op
import sqlalchemy as sa


revision = "0001_create_users_tasks"
down_revision = None
branch_labels = None
depends_on = None


user_role = sa.Enum("user", "admin", name="userrole")
task_status = sa.Enum("pending", "in_progress", "completed", name="taskstatus")
task_priority = sa.Enum("low", "medium", "high", name="taskpriority")


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("username", sa.String(length=50), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("role", user_role, nullable=False, server_default="user"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_users_id", "users", ["id"])
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_index("ix_users_username", "users", ["username"], unique=True)

    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.String(length=1000), nullable=True),
        sa.Column("status", task_status, nullable=False, server_default="pending"),
        sa.Column("priority", task_priority, nullable=False, server_default="medium"),
        sa.Column("due_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("owner_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_tasks_id", "tasks", ["id"])
    op.create_index("ix_tasks_owner_id", "tasks", ["owner_id"])


def downgrade() -> None:
    op.drop_index("ix_tasks_owner_id", table_name="tasks")
    op.drop_index("ix_tasks_id", table_name="tasks")
    op.drop_table("tasks")
    op.drop_index("ix_users_username", table_name="users")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_index("ix_users_id", table_name="users")
    op.drop_table("users")
