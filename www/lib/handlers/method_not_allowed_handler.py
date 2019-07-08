import flask
import http


def method_not_allowed_handler():
  return flask.Response(
      response=http.HTTPStatus.METHOD_NOT_ALLOWED)

