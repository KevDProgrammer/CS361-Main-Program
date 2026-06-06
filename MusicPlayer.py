# Note-4-Tester: MUST use python 3.12 or 3.13 for testing (pygame doesn't work on 3.14)
# ^^^ VERY IMPORTANT!!!

import time
import pygame

pygame.mixer.init()

# The database of available OSTs per title/page (based on title id match)
# (wav for terminal and mp3 for html)
music_map = {
    "Nier Replicant" : ["music/Song_of_the_Ancients_Devola.mp3", "music/His_Dream.mp3"],
    "Nier Automata" : ["music/Copied_City.mp3"],
    "Nier Reincarnation" : []
}

# to keep track of the current (starting) index of OSTs within a specific set (title)
current_selection = {
    "Nier Replicant" : 0,
    "Nier Automata" : 0,
    "Nier Reincarnation" : 0
}

previous_request = "" # for preventing repeatedly using the same request when shuffling to the next song 
with open("txt/music_request.txt", "w") as f: # clear any existing request left in the txt (for every new run)
    f.write("")

# open and read music_request.txt to access the user's current title-specific page by their id.
# it should hold something like: 
# action=play
# title=Nier Replicant (which matches html style).
def playback_request():
    content_data = {} # this stores the values that user have made & requested for

    with open("txt/music_request.txt", "r") as f:
        request = f.read().strip()

    for line in request.splitlines():
        key, value = line.split("=")
        content_data[key] = value

    action = content_data.get("action") # get the event for that action
    content_locator = content_data.get("title") # get the music files for that title

    return request, action, content_locator

# based on what title-specific page the user is on, sets of available music playback will be assigned,
# so eventually, the main program can call on it (by initating a play action). 
# Move selection index to next song if shuffle action is made instead.
def music_assignment(action, content_locator, music_map):
    # states no music snippets available were found for this title...
    unavailable_music = "Not available"
    if content_locator not in music_map:
         return unavailable_music
    if (len(music_map[content_locator]) == 0):
         return unavailable_music
    
    # p.s. NEW: added stop feature (same on html -> when clicked on), stop playing track (clear response).
    if action == "stop":
        pygame.mixer.music.stop()
        return "" 

    # move onto next track within the set if user clicked shuffle
    if action == "shuffle":
        current_selection[content_locator] += 1
        if (current_selection[content_locator] >= len(music_map[content_locator])):
            current_selection[content_locator] = 0  # loop back around to first song in set

    selection = music_map[content_locator][current_selection[content_locator]]

    pygame.mixer.music.load(selection)
    pygame.mixer.music.play()

    return selection

# open and write in response.txt to send the available music selections 
# for a specific title with the correct playback execution.
def playback_response(selection):
    with open("txt/music_response.txt", "w") as f:
        f.write(selection)

# continously check request for new updates (a proper looping)
# ...and the calls for all functions that are used
while True:
    time.sleep(0.1)

    try:
        request, action, content_locator = playback_request()
    except FileNotFoundError:
        continue

    # ignore empty requests or any unchanged requests
    if request == "" or request == previous_request:
        continue
    previous_request = request

    selection = music_assignment(action, content_locator, music_map)
    playback_response(selection)

# Order of execution:
# run this (and all other ms) first
# then run flaskServer
# open local website
# test