import click
import secrets
import string

from pathlib import Path

from db import DataBaseHandler
from config import DB_NAME, DB_PATH


def main() -> None:
    """Wrapper function for the CLI entry point."""
    if not (Path(DB_PATH) / DB_NAME).exists():
        db = DataBaseHandler()
        db.db_init()

    generate()


@click.command()
@click.option("--length", "-l", default=25, help="Length of the password to generate.")
def generate(length: int) -> str:
    """Generates a psudo random password of specified length and prints it to stdout.

    Args:
        length (int): The expected length of the generated password.

    Returns:
        str: The password.
    """
    alphabets = string.ascii_letters + string.digits + string.punctuation

    password = "".join(secrets.choice(alphabets) for _ in range(length))
    click.echo(password)
    return password


if __name__ == "__main__":
    main()
