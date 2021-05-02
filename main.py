
import flask

app = flask.Flask(__name__)

from flask import session
import requests

@app.route('/', methods=['GET', 'POST'])
def show_main():
    flickr_key = "d57e81fd7e74e169f325dff9c089283a"
    # if flask.request.method == 'POST':
    baseurl = "https://www.flickr.com/services/rest/"
    params_dict = {}
    params_dict["method"] = "flickr.photos.search"
    params_dict["api_key"] = flickr_key
    params_dict["tags"] = "rivers"
    params_dict["format"] = "json"
    params_dict["nojsoncallback"] = 1
    flickr_r = requests.get(baseurl, params = params_dict)
    print(flickr_r.url)
    data_json = flickr_r.json()["photos"]["photo"]
    context = {
        "photo": data_json
    }

    return flask.render_template("main.html", **context)

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