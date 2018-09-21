from pprint import pformat
import os

import requests
from flask import Flask, render_template, request, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.secret_key = "SECRETSECRETSECRET"
app.secret_token = os.environ["EVENTBRITE_TOKEN"]


@app.route("/")
def homepage():
    """Show homepage."""

    return render_template("homepage.html")


@app.route("/afterparty-search")
def show_afterparty_form():
    """Show afterparty finding form"""

    return render_template("afterparty-search.html")


@app.route("/afterparties")
def find_afterparties():
    """Search for afterparties on Eventbrite"""

    query = request.args.get('query')
    location = request.args.get('location')
    distance = request.args.get('distance')
    measurement = request.args.get('measurement')
    sort = request.args.get('sort')

    # If the required information is in the request, look for afterparties
    if location and distance and measurement:

        # The Eventbrite API requires the distance value to have a measurement
        distance = distance + measurement

        # TODO: Look for afterparties!

        # - Make a request to the Eventbrite API to search for events that match
        #   the form data.
        # - (Make sure to save the JSON data from the response to the data
        #   variable so that it can display on the page as well.)

        # data = {'This': ['Some', 'mock', 'JSON']}
        data2 = {'q': query , 'location.address' : location , 'location.within' : distance,
                'sort_by' : sort, 'token': app.secret_token}

        response = requests.get("https://www.eventbriteapi.com/v3/events/search",
                                params=data2)
        
        data = response.json()

        events = data['events']

        return render_template("afterparties.html",
                               data=pformat(data),
                               results=events)

    # If the required info isn't in the request, redirect to the search form
    else:
        flash("Please provide all the required information!")
        return redirect("/afterparty-search")


@app.route("/create-event", methods=['GET'])
def show_event_creation():
    """Show event creation page"""

    return render_template("event-creation.html")


@app.route("/create-event", methods=['POST'])
def create_eventbrite_event():
    """Create Eventbrite event using form data"""

    name = request.form.get('name')
    # The Eventbrite API requires the start & end times be in ISO8601 format
    # in the UTC time standard. Adding ':00' at the end represents the seconds,
    # and the 'Z' is the zone designator for the zero UTC offset.
    start_time = request.form.get('start-time') + ':00Z'
    end_time = request.form.get('end-time') + ':00Z'
    timezone = request.form.get('timezone')
    currency = request.form.get('currency')

    # TODO: Create my event!

    # - Make a request to the Eventbrite API to create a new event using the
    # form data and save the result in a variable called `json`.
    # - Flash add the created event's URL as a link to the success flash message

    ##### UNCOMMENT THIS once you make your request! #####
    # if response.ok:
    #     flash("Your event was created!")
    #     return redirect("/")
    # else:
    #     flash('OAuth failed: {}'.format(data['error_description']))
    #     return redirect("/create-event")

    return redirect("/")


############ Further Study ############

@app.route("/my-events")
def show_my_events():
    """Show a list of this app/user's Eventbrite events"""

    # Add your API request here.

    data = {'This': ['Some', 'mock', 'JSON']}  # Replace this with your response data

    events_dict = {}

    return render_template("my-events.html",
                           events=events_dict,
                           data=pformat(data))


# ############ Further Further Study ############

# @app.route("/register")
# def show_eventbrite_registration():
#     """Redirect user to Eventbrite's Approve/Deny page"""

#     return redirect("https://www.eventbrite.com/oauth/authorize"
#                     + "?response_type=code"
#                     + "&client_id=" + YOUR_EVENTBRITE_KEY_HERE)


# @app.route("/oauth")
# def oauth_process():
#     """Add bookmark for this event using OAuth"""

#     code = request.args.get('code')

#     # If Eventbrite returns an access code, use it to get an access token
#     # for the user and then add a bookmark for an event
#     if code:
#         access_token = get_access_token(code)

#         if access_token:
#             add_bookmark(access_token, '35827931307')

#     # If there is no access code, flash an error message
#     else:
#         flash('OAuth failed')

#     return redirect('/')


######### Helper Functions #########
def get_access_token(code):
    """Use access code to request user's access token"""

    # Add your post request here to get an access token
    # Call add_bookmark with your access token and event_id
    pass


def add_bookmark(access_token, event_id):
    """Use user's access token to save bookmark for event"""

    pass


if __name__ == "__main__":
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    DebugToolbarExtension(app)
    app.run(host="0.0.0.0")
