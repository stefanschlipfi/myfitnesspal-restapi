import flask
import json
import os
from werkzeug import exceptions
from datetime import datetime
import myfitnesspal
    
app = flask.Flask(__name__)

working_directory = "/opt/myfitnesspal-api"

myfitnesspal_users = dict()

def load_users_json():
    """
    load users json file 
    """

    try:
        with open(working_directory + "/users.json",'r') as jf:
            return json.load(jf)['users']
        
    except FileNotFoundError as e:
        raise  exceptions.InternalServerError(description="File Not found. Directory: {0}".format(working_directory + "/udsers.json"))
        
    except Exception as e:
        raise exceptions.InternalServerError(description=e)

def find_username_json(username):
    """
    find username in users.json
    """
    if not isinstance(username,str):
        raise exceptions.BadRequest(description="username musst be a str")

    users = load_users_json()
    if users:
        for user in users:
            if username in user['username']:
                return user

    raise exceptions.NotFound(description="username: {0} in users.json not found".format(username))

def load_myfitnesspal(username,password):
    try:
        user = myfitnesspal.Client(username,password)
    except Exception as e:
        raise e
    else:
        return user

def load_myfitnesspal_user(username):
    if username in myfitnesspal_users:
        return myfitnesspal_users[username]
    else:
        user = find_username_json(username)
        myfitnesspal_user = load_myfitnesspal(user['username'],user['password'])
        myfitnesspal_users.update({username:myfitnesspal_user})
        return myfitnesspal_user

@app.route("/today/meal/",methods=["GET"])
def meal_today():
    username = flask.request.args.get("username")
    if username:
        myfitnesspal_user = load_myfitnesspal_user(username)
        today = myfitnesspal_user.get_date(datetime.now())

        return flask.jsonify(today.get_as_dict())

@app.route("/today/progress/",methods=["GET"])
def progress_today():
    username = flask.request.args.get("username")
    if username:
        myfitnesspal_user = load_myfitnesspal_user(username)
        today = myfitnesspal_user.get_date(datetime.now())

        ### calculate progress ###
        progress = dict()
        for item in today.goals.keys():
            try:
                p = today.totals[item] - today.goals[item]
            except KeyError:
                p = 0 - today.goals[item]
            finally:
                progress.update({item:p})

        return flask.jsonify(progress)


if __name__ == '__main__':
    app.run()
