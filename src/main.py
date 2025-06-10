import getpass
import secrets
import string
from pathlib import Path

import click

from config import DB_NAME, DB_PATH
from crypto import Crypto
from db import DataBaseHandler
from tabulate import tabulate


@click.group()
@click.pass_context
def cli(ctx) -> None:
    """A command line password manager"""
    pass


@cli.command(
    "init",
    help="Initializes the database if it does not exits. Quits silently otherwise",
)
def initialize_vault() -> None:
    if not (Path(DB_PATH) / DB_NAME).exists():
        db = DataBaseHandler()
        db.db_init()
        click.echo(
            "Database initialized successfully. You can now set a master password."
        )
        crypt = Crypto(verification=False)
        master_password = prompt_master_password()
        key = crypt.generate_verification_key_from_master_password(master_password)
        db.set_key(key)
        click.echo("Master password set successfully. You can now use the vault.")

    return


@cli.command(help="Add an entry to the database")
@click.argument("service_name", type=str)
@click.argument("website", type=str)
@click.argument("username", type=str)
@click.argument("password", type=str)
@click.pass_context
def add(ctx, service_name: str, website: str, username: str, password: str) -> None:
    """Add an entry to the database.

    Args:
        service_name (str): Name of the service being used
        website (str): website uri
        username (str): username used in the website
        password (str): password used in the website
    """
    ctx.invoke(initialize_vault)
    cryp, master_password = prompt_and_verify_master_password()

    encrypted_username, encrypted_password = cryp.encrypt_username_password(
        username, password, master_password
    )

    db = DataBaseHandler()
    db.add_entry(
        service_name=service_name,
        website=website,
        username=encrypted_username,
        password=encrypted_password,
    )

    click.secho("Password saved successfully.", fg="green")


@cli.command(help="Remove a password based on index")
@click.argument("id", type=int)
def remove(id: int) -> None:
    if not (Path(DB_PATH) / DB_NAME).exists():
        click.secho(
            "There is no database to delete any entries. Create a database first.",
            fg="red",
        )
        return

    _, _ = prompt_and_verify_master_password()

    confirmation = (
        input(f"Are you sure you want to delete the entry number {id} [y/N]: ")
        .strip()
        .lower()
    )

    if confirmation == "y":
        db = DataBaseHandler()
        try:
            db.remove_entry(id)
            click.secho("Entry removed successfully.", fg="yellow")
        except Exception:
            click.secho("ID not found!! Nothing to delete.", fg="red")
        return

    click.echo("Entry was not removed.")


@cli.command(
    help="List all the entries without username and password. To view username and password, use the *view* command."
)
def list() -> None:
    if not (Path(DB_PATH) / DB_NAME).exists():
        click.secho(
            "There is no database to delete any entries. Create a database first.",
            fg="red",
        )
        return

    _, _ = prompt_and_verify_master_password()

    db = DataBaseHandler()
    data = db.list_all()
    click.echo(
        tabulate(
            data,
            headers=["ID", "Service Name", "Website"],
            tablefmt="pretty",
        )
    )
    return


@cli.command(help="View an individual entry")
@click.argument("id", type=int)
def view(id: int) -> None:
    crypt, master_password = prompt_and_verify_master_password()
    db = DataBaseHandler()
    try:
        data = db.get_entry(id)
    except ValueError:
        click.secho(
            "The given ID does not exist. Try again or use the list / search option.",
            fg="red",
        )
        return

    username, password = crypt.decrypt_username_password(
        data[3], data[4], master_password
    )

    click.echo(
        f"ID: {data[0]}\nService Name: {data[1]}\nWebsite: {data[2]}\nUsername: {username}\nPassword: {password}"
    )


@cli.command()
@click.option("--length", "-l", default=25, help="Length of the password to generate.")
def generate(length: int) -> str:
    """Generates a pseudo random password of specified length and prints it to stdout."""
    alphabets = string.ascii_letters + string.digits + string.punctuation

    password = "".join(secrets.choice(alphabets) for _ in range(length))
    click.echo(password)
    return password


def prompt_and_verify_master_password() -> tuple[Crypto, str]:
    master_password = prompt_master_password()
    cryp = Crypto()
    if not cryp.verify_master_password_from_key(master_password):
        click.secho("Invalid master password. Please try again.", fg="red")
        exit(1)
    return cryp, master_password


def prompt_master_password() -> str:
    """Prompts the user for a master password.

    Returns:
        str: The master password entered by the user.
    """
    return getpass.getpass("Enter your master password: ")


if __name__ == "__main__":
    cli()
