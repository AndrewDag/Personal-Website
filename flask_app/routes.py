# Author: Prof. MM Ghassemi <ghassem3@msu.edu>
from flask import current_app as app
from flask import render_template, redirect, request, session, url_for, copy_current_request_context
import os
import cgitb; cgitb.enable()
import os


APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route('/')
def root():
    return render_template("index.html")

@app.route('/personal-projects')
def personal():
    return render_template('personal_projects.html')

@app.route('/school-projects')
def school():
    return render_template('school_projects.html')

@app.route('/getimagefiles', methods = ["POST", "GET"])
def get_images():
    img_path = list(request.form.keys())[0]


    img_files = os.listdir(img_path)

    only_img_files = ""

    # Only extensions that should be used are image extensions (IMAGES SHOULD BE FORMATTED "name.extension" or else there is risk of breaking)
    for img in img_files:
        print(img)
        extension = img.split(".")[-1]
        print(extension)
        if extension == "png" or extension == "jpg" or extension == "jpeg" or extension == "gif":
            only_img_files += img + " "
        
    return only_img_files[:-1]
