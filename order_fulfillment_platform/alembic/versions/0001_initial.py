"""initial schema"""
from alembic import op
import sqlalchemy as sa
revision='0001';down_revision=None;branch_labels=None;depends_on=None
def upgrade():
    # Development shortcut: create from SQLAlchemy metadata. For production, generate a fully explicit migration with `alembic revision --autogenerate` and review it.
    from app.db.session import Base
    import app.db.base
    bind=op.get_bind(); Base.metadata.create_all(bind=bind)
def downgrade():
    from app.db.session import Base
    import app.db.base
    bind=op.get_bind(); Base.metadata.drop_all(bind=bind)
