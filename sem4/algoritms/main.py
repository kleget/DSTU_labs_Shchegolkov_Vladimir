import sys

from experiments import run_all_tasks


def setup_console_encoding() -> None:
    # Нужен UTF-8, чтобы русский текст корректно печатался в консоли.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")


if __name__ == "__main__":
    setup_console_encoding()
    run_all_tasks()
