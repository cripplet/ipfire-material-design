import flask
import http
import json

from lib.handlers import method_not_allowed_handler
from lib.handlers import not_found_handler


def _traverse_dict(d, path):
  d = dict(d)
  for p in path.split('/'):
    if not p:
      break
    if not (isinstance(d, list) or isinstance(d, dict)):
      raise IndexError
    try:
      d = d[p]
    except (KeyError, TypeError):
      d = d[int(p)]
  return d


def config_handler(path, config):
  try:
    return flask.Response(
        response=json.dumps(_traverse_dict(config, path), indent=4),
        status=http.HTTPStatus.OK,
        mimetype='application/json',
    )
  except (KeyError, IndexError, ValueError):
    return not_found_handler.not_found_handler()
