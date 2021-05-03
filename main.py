
import flask

app = flask.Flask(__name__)

from flask import session
import requests
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from io import StringIO
from io import BytesIO
import base64

@app.route('/', methods=['GET', 'POST'])
def show_main():
    return flask.render_template("main.html")

@app.route('/results', methods=['GET', 'POST'])
def show_results():
    if flask.request.method == 'POST':
        flickr_key = "d57e81fd7e74e169f325dff9c089283a"
        baseurl = "https://www.flickr.com/services/rest/"
        params_dict = {}
        params_dict["method"] = "flickr.photos.search"
        params_dict["api_key"] = flickr_key
        params_dict["tags"] = flask.request.form["tags"]
        params_dict["format"] = "json"
        params_dict["nojsoncallback"] = 1
        flickr_r = requests.get(baseurl, params = params_dict)
        print(flickr_r.url)
        data_json = flickr_r.json()["photos"]["photo"]
        
        urls = []

        for i in range(0, len(data_json)):
            url = "http://farm"+str(data_json[i]["farm"])+".staticflickr.com/"+str(data_json[i]["server"])+"/"+str(data_json[i]["id"])+"_"+str(data_json[i]["secret"])+".jpg"
            urls.append(url)
        
        context = {
            "photo": urls
        }

        return flask.render_template("results.html", **context)

@app.route('/selected', methods=['GET', 'POST'])
def show_selection():
    if "input-text" in flask.request.form:
        # Open an Image
        img = Image.open(BytesIO(requests.get(flask.request.form["img_url"]).content))

        # Call draw Method to add 2D graphis in an image
        I1 = ImageDraw.Draw(img)
        
        # Cutom font style and font size
        myFont = ImageFont.truetype('FreeMono.ttf', 65)

        # Add Text to an image
        I1.text((10, 10), flask.request.form["input-text"], font=myFont, fill =(0, 0, 0))

        output = BytesIO()
        img.save(output, "PNG")
        contents = base64.b64encode(output.getvalue())

        return flask.render_template("selected.html", old_img_url=flask.request.form["img_url"], img_data=contents.decode('utf-8'))

    else:
        return flask.render_template("selected.html", old_img_url=flask.request.form["img_url"])

