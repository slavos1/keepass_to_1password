import sys

import click
import twiggy

from .log import make_logger
from .parse import convert, info

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

logger = make_logger(__name__)

class Args:
    pass

pass_args = click.make_pass_decorator(Args, ensure=True)

def log_setup(level, stream=sys.stderr):
    output = twiggy.outputs.StreamOutput(twiggy.formats.line_format, stream=stream)
    twiggy.add_emitters(('*', twiggy.levels.name2level(level), True, output))

@click.group(context_settings=CONTEXT_SETTINGS)
#@click.version_option(VERSION, '--version', '-v')
@click.option('-d', '--debug', is_flag=True, help='Most verbose logging')
@click.option('-q', '--quiet', is_flag=True, help='Shows notices and worse')
@click.option('-i', '--input-file',
              type=click.File(),
              default='-',
              show_default=True,
              help='Input XML file created by KeePass export',
             )
@pass_args
def cli(common, debug, quiet, input_file):
    if debug:
        level = 'DEBUG'
    elif quiet:
        level = 'NOTICE'
    else:
        # verbose
        level = 'INFO'
    log_setup(level)
    common.input_file = input_file

@cli.command('convert')
@click.option('-g', '--group',
              required=True,
              help='Use entries only from this group; run "cli ... info" to see the group names',
             )
@click.option('-o', '--output-file',
              type=click.File('w'),
              default='-',
              show_default=True,
              help='''Output CSV file as per 1Password's requirements for "Logins"''',
             )
@click.option('-f', '--include',
              metavar='REGEX',
              help='Include only entries whose title matches this Python regex',
             )
@click.option('-x', '--exclude',
              metavar='REGEX',
              help='Exclude all entries whose title matches this Python regex',
             )
@pass_args
def _convert(common, group, output_file, include, exclude):
    '''Convert KeePass XML to 1Password-compatible CSV'''
    convert(common.input_file, group, output_file, include, exclude)

@cli.command('info')
@pass_args
def _info(common):
    '''Show group names in KeePass XML'''
    info(common.input_file)

