import typer


def main():
    typer.echo(f"Hello World")


def run_typer():
    typer.run(main)


if __name__ == "__main__":
    run_typer()
