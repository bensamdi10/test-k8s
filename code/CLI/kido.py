# coding: utf-8
import click
from utils.kido_cli import KidoCLI


class Config(object):

    def __init__(self):
        self.verbose = False
        self.kido_cli = KidoCLI()



pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group()
#@click.option('--verbose', id_flag=True)
@pass_config
def cli(config):
    pass

@cli.command()
@pass_config
def start(config):
    """ Start the Kido Server """
    click.echo("Start The Server")
    token = config.kido_cli.initCLI()
    click.echo(token)

@cli.command()
@pass_config
def stop(config):
    """ Stop the Kido Server """
    click.echo("The Server is Stopped CLI")

@cli.command()
@pass_config
def update(config):
    """ Update the Project in the Kido Server """
    click.echo("The Server is updated the Files for your project CLI")


