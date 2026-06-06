# the flask application itself (acting as the bridge between translating 
# our python microservice to our webpage, for web testing.)
# Flask Installation: run "python -m pip install flask" (in case you don't have flask yet)

# Order of Execution:
# 1. Run every MS (py) first
# 2. Run flaskServer
# 3. Run website with the local-host link
# (MUST RUN IN PYTHON VER 3.13 (pygame in music ms is VERY PICKY)!!!)

from flask import Flask, render_template, request, send_from_directory
import subprocess   # this built-in feature let flask to run our Resulter.py (microservice) simaltaniusly (as a seperate program)
import time

# set up the flask on web
app = Flask(__name__) 

@app.route('/')
def index():
    return render_template("home.html")

# make route to all html pages
@app.route('/home.html')
def home_page():
    return render_template("home.html")

@app.route('/search.html')
def search_page():
    return render_template("search.html")

@app.route('/search-genre-AA.html')
def genre_AA_search_page():
    return render_template("search-genre-AA.html")

@app.route('/help.html')
def help_page():
    return render_template("help.html")

@app.route('/sorted-rating.html')
def sorted_rating_page():
    return render_template("sorted-rating.html")

@app.route('/gp-nr.html')
def nier_replicant_page():
    return render_template("gp-nr.html")

@app.route('/gp-na.html')
def nier_automata_page():
    return render_template("gp-na.html")

@app.route('/gp-nr2.html')
def nier_reincarnation_page():
    return render_template("gp-nr2.html")

# make route to all js and styles
@app.route('/style-s.css')
def css():
    return send_from_directory("templates", "style-s.css")

@app.route('/sound.js')
def sound_js():
    return send_from_directory("templates", "sound.js")

# make route to all relevant folders
@app.route('/images/<name>')
def images(name):
    return send_from_directory("images", name)

@app.route("/sounds/<name>")
def sounds(name):
    return send_from_directory("sounds", name)

# THE SEARCH MS ROUTE: 
# when user submits the search form, flask will access the given user-input from the html form, and it'll write said input into search_request.txt.
# in short, this is the user-input + update search_request.txt section.
@app.route('/search', methods=["POST"])     # matching the calls http call as established in the web page
def searching():
    user_search = request.form["game"] # (access input from the html form)

    with open("txt/search_request.txt", "w") as f: # (write it into request)
        f.write(user_search)

    # run the microservice now, directly here.
    # after comparison of user-input search and available matches in the database.txt...
    # ...the result will be written in the search_respnose.txt...
    subprocess.run(["python", "Resulter.py"])

    # ...once result is in the search_response.txt, the program read it...
    with open("txt/search_response.txt", "r") as f:
        result = f.read().strip()

    # ...if no matches, send user to the search.html page (holding no result)...
    if (result == "No matches found"):
        return render_template("search.html", result="none")
    else:
        return render_template(result)     # ...otherwise it works, redirect user to the content page that matches their search.

# THE MUSIC MS SECTION (with routes):
@app.route("/connect.js")
def connect_js():
    return send_from_directory("templates", "connect.js")

@app.route("/music", methods=["POST"])
def music_manager():
    data = request.get_json() # retireved from connect.js
    action = data["action"]
    title = data["title"]

    with open("txt/music_request.txt", "w") as f: # return the selected song back
        f.write(f"action={action}\n")
        f.write(f"title={title}")

    return "music flask execuded" # confirm it works

# THE IMAGE GALLERY MS SECTION (with routes):
# (make the image section on the game page into a clcikable slideshow)
@app.route("/connection.js")
def connection_js():
    return send_from_directory("templates", "connection.js")

@app.route("/gallery", methods=["POST"])
def gallery_manager():
    data = request.get_json() # retireved from connection.js
    action = data["action"]
    title = data["title"]
    request_id = data["request_id"] # now, every previous request logged will have a different id attributes, allowing for repeated click of the same button...

    with open("txt/image_request.txt", "w") as f: # return the selected image back
        f.write(f"action={action}\n")
        f.write(f"title={title}\n")
        f.write(f"request_id={request_id}") 

    # the display will then hold the final image path for the gallery
    time.sleep(0.2) # slightly sloweer than the ms itself, just to play it safe (response don't overlap or glitches when changing img)
    with open("txt/image_response.txt", "r") as f:
        display = f.read().strip()
    return display

# THE RATING MS SECTION (with routes):
# (holds rating scores (for each game title/gp) + sorting titles in order (highest to lowest))
@app.route("/bridge.js")
def bridge_js():
    return send_from_directory("templates", "bridge.js")

@app.route("/rating", methods=["POST"])
def rating_manager():
    data = request.get_json()
    action = data["action"]
    title = data["title"]

    with open("txt/rating_request.txt", "w") as f:
        f.write(f"action={action}\n")
        f.write(f"title={title}")

    # the display then holds the result within response for the ratings
    time.sleep(0.2)
    with open("txt/rating_response.txt", "r") as f:
        rating_response = f.read()
    return rating_response

# for running the Flask server
if __name__ == "__main__":
    app.run(debug=True)