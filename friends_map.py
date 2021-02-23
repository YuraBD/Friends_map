'''
This is module to make a map of friends of given user

It has 4 functions:

1) make_json
Return json object of friend of given user.
user - username of Twitter user
friends_number - number of friends to show
bearer token - bearer token which twitter users with
developer accounts have.

2) information
Display a page where user enters username,
friends_number, bearer_token

3) make_map
Make a map. Use username, friends_number, bearer_token which
user entrered in information.html

4) friends_map
Display a map page
'''
import folium
from geopy.geocoders import Nominatim
import requests
from flask import Flask, render_template, request


app = Flask(__name__)
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True

def make_json(user, friends_number, bearer_token):
    '''
    Return json object of friend of given user.
    user - username of Twitter user
    friends_number - number of friends to show
    bearer token - bearer token which twitter users with
     developer accounts have.
    '''
    base_url = "https://api.twitter.com/"
    search_url = f"{base_url}1.1/friends/list.json"
    search_headers = {
        "Authorization": f"Bearer {bearer_token}"
    }
    search_params = {
        'screen_name': user,
        'count': friends_number
    }
    response = requests.get(search_url, headers=search_headers,\
                            params=search_params)
    json_response = response.json()
    return json_response


@app.route("/")
def information():
    '''
    Display a page where user enters username,
     friends_number, bearer_token

    '''
    return render_template('information.html')


def make_map():
    '''
    Make a map. Use username, friends_number, bearer_token which
    user entrered in information.html
    '''
    user = request.form.get("username")
    friends_number = int(request.form.get("friends_number"))
    bearer_token = request.form.get("bearer_token")
    geolocator = Nominatim(user_agent="friends_map")
    frieds_json = make_json(user, friends_number, bearer_token)
    f_map = folium.Map()
    fg = folium.FeatureGroup(name="Friends")
    for user in frieds_json['users']:
        try:
            location = geolocator.geocode(user['location'])
            coords = (location.latitude, location.longitude)
        except AttributeError:
            continue
        name = user['screen_name']
        fg.add_child(folium.Marker(location=coords,
                                   popup=name,
                                   icon=folium.Icon()))
    f_map.add_child(fg)
    f_map.save('templates/map.html')


@app.route("/friends_map", methods=["POST"])
def friends_map():
    '''
    Display a map page
    '''
    make_map()
    return render_template('map.html')


if __name__ == "__main__":
    app.run(debug=True)
