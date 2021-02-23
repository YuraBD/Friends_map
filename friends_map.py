'''
'''
import folium
from geopy.geocoders import Nominatim
import json
import requests
from flask import Flask, render_template, request


app = Flask(__name__)
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True

def make_json(user, friends_number, bearer_token):
    '''
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
    response = requests.get(search_url, headers=search_headers, params=search_params)
    json_response = response.json()
    return json_response


@app.route("/")
def information():
    '''
    '''
    return render_template('information.html')


def make_map():
    '''
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
    '''
    make_map()
    return render_template('map.html')


if __name__ == "__main__":
    app.run(debug=True)