import re
import sys
import csv
from functools import partial
from base64 import b64decode
from binascii import hexlify

from lxml import etree

from .log import make_logger

logger = make_logger(__name__)

MANDATORY_FIELDS = [
    'title',
    'website',
    'username',
    'password',
    'notes',
]

def get_simple(xml, key):
    return xml.xpath(key + '/text()')[0]

def get_key(xml, key, optional=True, title=None):
    try:
        return xml.xpath('*[Key/text()="{}"]/Value/text()'.format(key))[0]
    except:
        if not optional:
            raise
        logger.debug('Error occurred for key {!r} of entry {!r}: {}',
                     key, title, sys.exc_info()[1])

def _iter(xml, include, exclude):
    for entry in xml.xpath('Entry[Times/Expires/text()="False"]'):
        title = get_key(entry, 'Title', optional=False)
        if include and not include.search(title):
            logger.debug('Ignoring entry {!r} as not to be included', title)
            continue
        if exclude and exclude.search(title):
            logger.debug('Ignoring entry {!r} as to be excluded', title)
            continue
        uuid = hexlify(b64decode(get_simple(entry, 'UUID'))).decode('ascii')
        logger.debug('Found entry with title {!r} (with id={!r})', title, uuid)
        get_other_field = partial(get_key, entry, title=title)
        row = {
            'title': title,
            'uuid': uuid,
            'website': get_other_field('URL'),
            'username': get_other_field('UserName'),
            'password': get_other_field('Password'),
            'notes': get_other_field('Notes'),
        }
        #logger.debug('{!r}', row)
        yield row

def find_group(xml, name):
    try:
        return xml.xpath('//Group[Name/text() = "{}"]'.format(name))[0]
    except:
        raise InvalidGroup('{!r} -- no such group; run "cli ... info" to see all valid groups'.format(name))

class InvalidGroup(ValueError):
    pass

def _parse(input_file, group=None, output_file=None, include=None, exclude=None, show_info=False):
    xml = etree.parse(input_file)
    if show_info:
        for g in xml.xpath('//Group'):
            logger.notice('Found group {!r}', get_simple(g, 'Name'))
        return
    logger.info('converting {} -> {}', input_file.name, output_file.name)
    logger.debug('xml={!r}', xml)
    group = find_group(xml, group)
    out = csv.writer(output_file)
    rows = 0
    if include:
        include = re.compile(include, re.IGNORECASE)
    if exclude:
        exclude = re.compile(exclude, re.IGNORECASE)
    for row in sorted(_iter(group, include, exclude), key=lambda x:x['title'].lower()):
        logger.notice('Writing entry with title {title!r} (with id={uuid!r})', **row)
        out.writerow([row[k] for k in MANDATORY_FIELDS])
        rows += 1
    logger.notice('Wrote {} rows to {}', rows, output_file.name)

def convert(input_file, group, output_file, include=None, exclude=None):
    return _parse(input_file, group, output_file, include, exclude)

def info(input_file):
    return _parse(input_file, show_info=True)

