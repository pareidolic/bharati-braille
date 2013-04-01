# vim: set sts=4 sw=4 et :
import sys

from bottle import route, run, get, request, static_file, template
from backend.converters import convert_devanagari_to_braille

if sys.version_info.major != 3:
    raise Exception("This program needs Python 3!")

@route("/", method=["POST", "GET"])
def index():
    input_text = request.forms.devanagari
#    input_text = "कर अपनी शायरी की दुनिया में आ बैठा और तीन ही साल की मश्क़ ने मेरी कल्पना के जौहर खोल"
    braille = convert_devanagari_to_braille(input_text)
    return template("index", input_text=input_text, braille=braille)

@get("/<filetype:re:(js|static)>/<filepath:path>")
def server_static(filetype, filepath):
    return static_file(filepath, root="./{0}".format(filetype))

@get("/<text>")
def echo(text=""):
    return text

if __name__ == "__main__":
    run(host="brailleconverter.pareidolic.in", port=8080)