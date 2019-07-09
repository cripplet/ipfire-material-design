import json

from lib.handlers import shared


def version_handler():
  with open('config/api_version.json') as fp:
    return shared.json_handler(json.loads(fp.read()))
