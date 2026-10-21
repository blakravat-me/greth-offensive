"""Root-level wrapper used by the project script entry point."""

from greth.main import run


if __name__ == "__main__":
    raise SystemExit(run())
