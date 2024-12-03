#!/usr/bin/env python3
import os
import sys
import argparse
from alembic import command
from alembic.config import Config

def get_alembic_config():
    """Get Alembic configuration"""
    config = Config("migrations/alembic.ini")
    config.set_main_option("script_location", "migrations")
    return config

def upgrade_db(revision='head'):
    """Upgrade database to a later version."""
    alembic_cfg = get_alembic_config()
    command.upgrade(alembic_cfg, revision)

def downgrade_db(revision):
    """Revert database to a previous version."""
    alembic_cfg = get_alembic_config()
    command.downgrade(alembic_cfg, revision)

def create_migration(message):
    """Create a new migration."""
    alembic_cfg = get_alembic_config()
    command.revision(alembic_cfg, message=message, autogenerate=True)

def show_history():
    """Show migration history."""
    alembic_cfg = get_alembic_config()
    command.history(alembic_cfg)

def main():
    parser = argparse.ArgumentParser(description='Database migration manager')
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Upgrade command
    upgrade_parser = subparsers.add_parser('upgrade', help='Upgrade database')
    upgrade_parser.add_argument('--revision', default='head',
                              help='Revision to upgrade to (default: head)')

    # Downgrade command
    downgrade_parser = subparsers.add_parser('downgrade', help='Downgrade database')
    downgrade_parser.add_argument('revision', help='Revision to downgrade to')

    # Create migration command
    create_parser = subparsers.add_parser('create', help='Create new migration')
    create_parser.add_argument('message', help='Migration message')

    # History command
    subparsers.add_parser('history', help='Show migration history')

    args = parser.parse_args()

    try:
        if args.command == 'upgrade':
            print(f"Upgrading database to {args.revision}...")
            upgrade_db(args.revision)
            print("Database upgrade completed successfully!")

        elif args.command == 'downgrade':
            print(f"Downgrading database to {args.revision}...")
            downgrade_db(args.revision)
            print("Database downgrade completed successfully!")

        elif args.command == 'create':
            print(f"Creating new migration: {args.message}")
            create_migration(args.message)
            print("Migration created successfully!")

        elif args.command == 'history':
            print("Migration history:")
            show_history()

        else:
            parser.print_help()
            sys.exit(1)

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
