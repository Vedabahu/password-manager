import secrets
import string
from pathlib import Path
import getpass

import click

from config import DB_NAME, DB_PATH
from db import DataBaseHandler
from crypto import Crypto


def main() -> None:
    """Wrapper function for the CLI entry point."""
    if not (Path(DB_PATH) / DB_NAME).exists():
        db = DataBaseHandler()
        db.db_init()
        click.echo(
            "Database initialized successfully. You can now set a master password."
        )
        crypt = Crypto(verification=False)
        master_password = getpass.getpass("Enter your master password: ")
        key = crypt.generate_verification_key_from_master_password(master_password)
        db.set_key(key)
        click.echo("Master password set successfully. You can now use the vault.")

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
