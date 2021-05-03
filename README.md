# umich-academic-innovation-task
This is a repo for coding challenge for Academic Innovation Summer Fellowship 2021.

Meme generator makes use of the Flickr API and provides an input that allows a user to search for images on Flickr that match a given string. Search results are presented and then allow a user to select one. After selection, allow a user to enter some text to the image, and the user can click the image and download the new image.

## Installation
Download the repo.
Please create a Python virtual environment for running the webiste, and activate the venv when running the code in the repo.
 ```
 $ pwd
   /umich-academic-innovation-task
 $ python3 -m venv env
 $ source env/bin/activate
 ```
You may exit the venv by ```deactivate``` command when you need.
```
$ deactivate
```

## Usage
```
 (env) $ pwd
         /umich-academic-innovation-task
 (env) $ ./run
```
Then you can navigate to http://localhost:8000 and see the webiste meme generator.

Note: You may need to install packages needed if prompts like "no module named PIL" is found.
