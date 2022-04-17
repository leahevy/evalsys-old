import sys
import traceback

import click
import typer

_app = typer.Typer(
    help="Tool to configure Linux based systems including population of dotfiles and package installation."
)


@_app.command()
def main(
    debug: bool = typer.Option(False, "--debug", "-d", help="Run in debug mode"),
    dry_run: bool = typer.Option(
        False, "--dry-run", "-n", help="Only print the operations. Don't do anyting"
    ),
):
    typer.echo(f"Hello World")


def run_cli_standalone():
    command = typer.main.get_command(_app)

    debug = {"-d", "--debug"}.intersection(sys.argv)
    try:
        result = command(standalone_mode=False)
    except click.exceptions.Abort:
        print("Execution was aborted.", file=sys.stderr)
        result = 2
    except Exception as e:
        if str(e) == "Missing command.":
            sys.argv += ["--help"]
            command(standalone_mode=False)
            print("\nError: Missing command.")
            result = 3
        elif "No such command '" in str(e):
            sys.argv += ["--help"]
            command()
            raise  # Never reached
        elif "Got unexpected extra argument (" in str(e):
            sys.argv += ["--help"]
            command(standalone_mode=False)
            print(f"\n{str(e)}")
            result = 4
        else:
            print("Error:", file=sys.stderr)
            if debug:
                print(traceback.format_exc(), file=sys.stderr)
            else:
                print(str(e), file=sys.stderr)
            result = 1

    sys.exit(result)


if __name__ == "__main__":
    run_cli_standalone()
