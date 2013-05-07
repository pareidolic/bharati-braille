# vim: set sts=4 sw=4 et :
import sys

from bottle import route, run, get, request, static_file, template
from backend.converters import convert_any_indic_to_braille

if sys.version_info.major != 3:
    raise Exception("This program needs Python 3!")

@route("/", method=["POST", "GET"])
def index():
    input_text = request.forms.devanagari
    (braille, warnings) = ("", "")
    if input_text:
        (braille, warnings) = convert_any_indic_to_braille(input_text)
    return template("index", 
                    input_text=input_text,
                    braille=braille,
                    warnings=warnings)

@get("/<filetype:re:(js|static)>/<filepath:path>")
def server_static(filetype, filepath):
    return static_file(filepath, root="./{0}".format(filetype))

@get("/<favicon:re:.*\.(ico|png)>")
def server_static(favicon):
    return static_file(favicon, root="./")

@get("/<filename>.html")
def serve_html(filename):
    return static_file("{0}.html".format(filename), root="./")

if __name__ == "__main__":
    run(host="bharati-braille.pareidolic.in", port=8080)
