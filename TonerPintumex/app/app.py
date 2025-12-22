from flask import Flask, jsonify
import pkgutil
import importlib
import os
import sys

# Ensure project root is on sys.path so `importlib.import_module('app.routes')`
# works when running this file directly (python app/app.py).
_ROOT = os.path.dirname(os.path.dirname(__file__))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask!"

def _register_route_blueprints():
    package_name = 'app.routes'
    try:
        pkg = importlib.import_module(package_name)
    except Exception:
        print(f"[routes] could not import {package_name}")
        return

    registered = []
    for _, module_name, _ in pkgutil.iter_modules(pkg.__path__):
        module = importlib.import_module(f"{package_name}.{module_name}")
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            try:
                from flask import Blueprint
                if isinstance(attr, Blueprint):
                    app.register_blueprint(attr, url_prefix='/api')
                    registered.append((module_name, attr_name))
            except Exception:
                continue

    if registered:
        print('[routes] registered blueprints:')
        for mod, name in registered:
            print(f'  - {mod}.{name}')
    else:
        print('[routes] no blueprints registered')


_register_route_blueprints()


if __name__ == '__main__':
    app.run()