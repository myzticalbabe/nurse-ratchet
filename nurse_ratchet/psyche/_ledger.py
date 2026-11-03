# coding: utf-8
"""Local failure ledger for Nurse Ratchet standalone package.

This module replaces the CORE.failure_ledger dependency so the package
can run standalone without the monorepo. It provides a minimal
note_failure function that writes to a local file and logs.
"""

from __future__ import annotations

import json
import os
import sys
import threading
from pathlib import Path
from typing import Optional

# Thread-safe file writing
_LEDGER_LOCK = threading.Lock()
_LEDGER_PATH: Optional[Path] = None


def _get_ledger_path() -> Path:
    """Get or create the ledger file path."""
    global _LEDGER_PATH
    if _LEDGER_PATH is None:
        # Use a local file in the package directory
        pkg_dir = Path(__file__).parent
        _LEDGER_PATH = pkg_dir / "failure_ledger.jsonl"
    return _LEDGER_PATH


def note_failure(where: str, exc: Optional[BaseException] = None) -> None:
    """Record a failure to the local ledger.

    Args:
        where: Context string describing where the failure occurred
        exc: Optional exception that triggered the failure
    """
    ledger_path = _get_ledger_path()
    entry = {
        "where": where,
        "exc_type": type(exc).__name__ if exc else None,
        "exc_msg": str(exc) if exc else None,
        "pid": os.getpid(),
    }
    line = json.dumps(entry, ensure_ascii=False)
    with _LEDGER_LOCK:
        try:
            with ledger_path.open("a", encoding="utf-8") as f:
                f.write(line + "\n")
        except OSError:
            # If we can't write, fall back to stderr
            print(f"[NURSE_RATCHET LEDGER] {line}", file=sys.stderr)


# For backward compatibility with code that checks this
_LEDGER_IMPORT_ERROR: Optional[str] = None
try:
    # Verify the ledger is writable
    _get_ledger_path().touch(exist_ok=True)
except OSError as _e:
    _LEDGER_IMPORT_ERROR = str(_e)