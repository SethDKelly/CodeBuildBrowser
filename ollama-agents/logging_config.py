import logging
from logging import StreamHandler, FileHandler, Formatter
from pathlib import Path


def configure_logging(log_file: str | None = None, level: int = logging.INFO):
    """Configure root logging for the application.

    - Adds a console handler and optional file handler.
    - Keeps formatting concise.
    """
    root = logging.getLogger()
    if root.handlers:
        # Already configured
        return

    root.setLevel(level)

    fmt = Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s", "%Y-%m-%d %H:%M:%S")

    ch = StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(fmt)
    root.addHandler(ch)

    if log_file:
        p = Path(log_file)
        p.parent.mkdir(parents=True, exist_ok=True)
        fh = FileHandler(p, encoding="utf-8")
        fh.setLevel(level)
        fh.setFormatter(fmt)
        root.addHandler(fh)
