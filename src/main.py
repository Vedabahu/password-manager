import click
import secrets
import string


def main() -> None:
    """Wrapper function for the CLI entry point."""
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
