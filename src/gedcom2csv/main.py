import logging
import os

import click

from gedcom2csv.transformer import Gedcom2CSV

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO").upper())
logger = logging.getLogger()


@click.group()
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)


@cli.command(help="Convert a GEDCOM file into a CSV string")
@click.argument("gedcom-file")
@click.pass_context
def convert(ctx, gedcom_file: str):
    if not os.path.isfile(gedcom_file):
        raise ValueError(f"{gedcom_file} does not exist")

    converter = Gedcom2CSV()
    graph_string = converter.convert_to_csv(gedcom_file)
    print(graph_string)


if __name__ == "__main__":
    cli(obj={})
