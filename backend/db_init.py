"""
db_init.py — VocalGuard database bootstrap helper
===================================================

Safely initialises a fresh, *empty* ``vocalguard.db`` on a developer's
machine or a deployment target.

Why this exists (see issue #2)
-------------------------------
The ``vocalguard.db`` file was previously committed to the repository.
Compatible with Python 3.8+.
That is a security problem because:

  * The database may contain real user data (calls, email addresses,
    password hashes, PII from call transcripts).
  * Binary blobs bloat the repository history and cannot be force-pushed
    away without rewriting history for every contributor.

The file is now excluded from Git via ``.gitignore``.  Run this script
once after a fresh clone to create an empty, schema-only database:

    cd backend
    python db_init.py

Usage
-----
    python db_init.py [--db-path PATH]

    --db-path   Override the database file location.
                Defaults to the value of the DB_PATH environment variable,
                or ``backend/vocalguard.db`` relative to this file.
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Resolve the database path using the same priority as VocalGuardDB.__init__
# ---------------------------------------------------------------------------

def resolve_db_path(override: Optional[str] = None) -> Path:
    if override:
        return Path(override)
    env_path = os.getenv("DB_PATH", "").strip()
    if env_path:
        return Path(env_path)
    return Path(__file__).parent / "vocalguard.db"


def init_database(db_path: Path) -> None:  # noqa: PLC0415
    """Create the database schema without inserting any data."""
    # Import here so the script can be run from the repo root too
    sys.path.insert(0, str(Path(__file__).parent))
    from database import VocalGuardDB  # noqa: PLC0415

    db_path.parent.mkdir(parents=True, exist_ok=True)
    db = VocalGuardDB(db_path=str(db_path))
    print(f"[db_init] Database initialised at: {db_path.resolve()}")
    print("[db_init] Schema created (no data inserted).")
    print(
        "[db_init] Reminder: this file is listed in .gitignore — "
        "do NOT commit it to the repository."
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Initialise the VocalGuard SQLite database schema."
    )
    parser.add_argument(
        "--db-path",
        default=None,
        metavar="PATH",
        help=(
            "Path for the database file. "
            "Defaults to DB_PATH env var or backend/vocalguard.db."
        ),
    )
    args = parser.parse_args()

    db_path = resolve_db_path(args.db_path)

    if db_path.exists():
        print(f"[db_init] Database already exists at: {db_path.resolve()}")
        print("[db_init] Nothing to do. Delete the file first to re-initialise.")
        sys.exit(0)

    init_database(db_path)


if __name__ == "__main__":
    main()
