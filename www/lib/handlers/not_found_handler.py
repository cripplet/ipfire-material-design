import flask
import http


def not_found_handler():
  return flask.Response(
      status=http.HTTPStatus.NOT_FOUND)
