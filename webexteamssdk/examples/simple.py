#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""Simple webexteamssdk demonstration script.

Very simple script to create a demo room, post a message, and post a file.
If one or more rooms with the name of the demo room already exist, it will
delete the previously existing rooms.

The package natively retrieves your Webex Teams access token from the
WEBEX_TEAMS_ACCESS_TOKEN environment variable.  You must have this environment
variable set to run this script.


Copyright (c) 2016-2020 Cisco and/or its affiliates.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


from __future__ import print_function
from webexteamssdk import WebexTeamsAPI


DEMO_ROOM_NAME = "webexteamssdk Demo Room"
DEMO_PEOPLE = ["test01@cmlccie.com", "test02@cmlccie.com"]
DEMO_MESSAGE = u"Webex Teams rocks!  \ud83d\ude0e"
DEMO_FILE_URL = \
    "https://www.webex.com/content/dam/wbx/us/images/dg-integ/teams_icon.png"


# Create a WebexTeamsAPI connection object; uses your WEBEX_TEAMS_ACCESS_TOKEN
api = WebexTeamsAPI()


# Clean up previous demo rooms
print("Searching for existing demo rooms...")

# Create a generator container (iterable) that lists the rooms where you are
# a member
rooms = api.rooms.list()

# Build a list of rooms with the name DEMO_ROOM_NAME
existing_demo_rooms = [room for room in rooms if room.title == DEMO_ROOM_NAME]
if existing_demo_rooms:
    print("Found {} existing room(s); deleting them."
          "".format(len(existing_demo_rooms)))
    for room in existing_demo_rooms:
        # Delete the room
        api.rooms.delete(room.id)
        print("Room '{}' deleted.".format(room.id))


# Create a new demo room
demo_room = api.rooms.create(DEMO_ROOM_NAME)

# Print the room details (formatted JSON)
print(demo_room)

for person_email in DEMO_PEOPLE:
    # Add people to the room
    api.memberships.create(demo_room.id, personEmail=person_email)

# Create a message in the new room
message = api.messages.create(demo_room.id, text=DEMO_MESSAGE)

# Print the message details (formatted JSON)
print(message)

# Post a file in the new room from test_url
message = api.messages.create(demo_room.id, files=[DEMO_FILE_URL])

# Print the message details (formatted JSON)
print(message)
