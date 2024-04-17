import os
import sys
from logging.config import fileConfig

from alembic import context
from dotenv import dotenv_values,load_dotenv

from sqlalchemy import engine_from_config, pool

import src.entity.models

import alembic_autogenerate_enums

from src.entity.db import Base

sys.path.append(os.getcwd())

config = context.config

fileConfig(config.config_file_name)

target_metadata = Base.metadata

load_dotenv()


def run_migrations_offline():
    """Run migrations in 'offline' mode.
    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.
    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.
    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_schemas=True,
        )

        with context.begin_transaction():
            context.run_migrations()


env = dotenv_values('.env')
config.set_main_option('sqlalchemy.url',  os.environ.get('DATABASE_URI'))

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
