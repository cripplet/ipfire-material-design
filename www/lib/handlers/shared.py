import flask
import http
import json

from lib.handlers import method_not_allowed_handler
from lib.handlers import not_found_handler


def json_handler(config):
  return flask.Response(
      response=json.dumps(config, indent=4),
      status=http.HTTPStatus.OK,
      mimetype='application/json',
  )
