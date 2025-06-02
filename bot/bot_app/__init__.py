import logging

from .app import dp
from . import commands, button_signature, data_fetcher, \
    keyboards, state, services, local_settings


logging.basicConfig(level=logging.INFO)
