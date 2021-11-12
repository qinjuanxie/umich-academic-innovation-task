
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
import textwrap

@app.route('/', methods=['GET', 'POST'])
def show_main():
    return flask.render_template("main.html")

@app.route('/results', methods=['GET', 'POST'])
def show_results():
    flickr_key = "YOUR-OWN-PRIVATE-KEY-HERE"  # Use your Flicker account private key
    baseurl = "https://www.flickr.com/services/rest/"
    params_dict = {}
    params_dict["method"] = "flickr.photos.search"
    params_dict["api_key"] = flickr_key
    params_dict["tags"] = flask.request.form["tags"]
    params_dict["format"] = "json"
    params_dict["nojsoncallback"] = 1
    flickr_r = requests.get(baseurl, params = params_dict)
    data_json = flickr_r.json()["photos"]["photo"]
    
    urls = []

    for i in range(0, len(data_json)):
        url = "http://farm"+str(data_json[i]["farm"])+".staticflickr.com/"+str(data_json[i]["server"])+"/"+str(data_json[i]["id"])+"_"+str(data_json[i]["secret"])+".jpg"
        urls.append(url)
    
    context = {
        "size": len(urls),
        "photo": urls
    }

    return flask.render_template("results.html", **context)

@app.route('/selected', methods=['GET', 'POST'])
def show_selection():
    if "input-text" in flask.request.form:
        # Open an Image
        img = Image.open(BytesIO(requests.get(flask.request.form["img_url"]).content))

        # Call draw Method to add 2D graphis in an image
        draw = ImageDraw.Draw(img)
        
        # Cutom font style and font size
        myFont = ImageFont.truetype('FreeMono.ttf', 30)

        # Add Text to an image
        # Wrap it if too long
        lines = textwrap.wrap(text=flask.request.form["input-text"], width=20)
        img_w,img_h = img.size
        y_text = 0
        for line in lines:
            line_w, line_h = myFont.getsize(line)
            draw.text(((img_w - line_w) / 2, y_text), line, font=myFont, fill=(255,203,5))
            y_text += line_h

        output = BytesIO()
        img.save(output, "PNG")
        contents = base64.b64encode(output.getvalue())

        return flask.render_template("selected.html", old_img_url=flask.request.form["img_url"], img_data=contents.decode('utf-8'))

    else:
        return flask.render_template("selected.html", old_img_url=flask.request.form["img_url"])

