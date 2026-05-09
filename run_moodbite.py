import importlib.util
import os
import sys
import webbrowser
from threading import Timer


def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__)))
    return os.path.join(base_path, relative_path)


os.chdir(resource_path("."))

spec = importlib.util.spec_from_file_location("moodbite_app", resource_path("app.py"))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


if __name__ == "__main__":
    url = "http://127.0.0.1:5000/"
    Timer(1.2, lambda: webbrowser.open(url)).start()
    module.app.run(host="127.0.0.1", port=5000, debug=True, use_reloader=False)
