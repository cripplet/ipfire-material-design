from lib.app import app
from lib.app import routes
from lib.app import errors


def main():
  for r in routes.ROUTES:
    app.app.add_url_rule(
        rule=r['rule'],
        endpoint=r['endpoint'],
        view_func=r['view_func'],
        provide_automatic_options=r['provide_automatic_options'],
        **r['options'])
  for h in errors.ERROR_HANDLERS:
    app.app.register_error_handler(
        code_or_exception=h['code_or_exception'],
        f=h['f'])

  app.app.run(debug=True, host='0.0.0.0', port=8080)


if __name__ == '__main__':
  main()
