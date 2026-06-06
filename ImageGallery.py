import time

# The database of available images for each title/page (grouped by title id)
gallery_map = {
    "Nier Replicant" : ["images/Nier_Replicant_Photo.jpg", "images/Nier_Replicant_Photo_2.jpg", "images/Nier_Replicant_Photo_3.jpg", "images/Nier_Replicant_Photo_4.jpg", "images/Nier_Replicant_Photo_5.jpg"],
    "Nier Automata" : ["images/Nier_Automata_Photo.jpg", "images/Nier_Automata_Photo_2.jpg", "images/Nier_Automata_Photo_3.jpg"],
    "Nier Reincarnation" : ["images/Nier_Reincarnation_Photo.jpg", "images/Nier_Reincarnation_Photo_2.jpg"]
}

# To keep track of the current (starting) index of images within a specific set (title)
current_image = {
    "Nier Replicant" : 0,
    "Nier Automata" : 0,
    "Nier Reincarnation" : 0
}

previous_request = ""

# Open and read image_request.txt for the current page (by title id) that the user is on...
# then gathers relevant button action info for the MS, in this form (example):
# action=left           (left button clicked...)
# title=Nier Replicant  (...on/for this topic)
def gallery_request():
    gallery_data = {} # this stores the values that user have made & requested for

    with open("txt/image_request.txt", "r") as f:
        request = f.read().strip()

    for line in request.splitlines():
        key, value = line.split("=")
        gallery_data[key] = value

    action = gallery_data.get("action") # get the event for that action (clicked)
    content_locator = gallery_data.get("title") # get the images path for that title (action made)

    return request, action, content_locator

# Based on what button actions (start-jumper, previous, next, and end-jumper) were taken, 
# and what page (title based) user is on, shift list index accordingly and assign the
# image path for execution (display).
# note: first (left-most starting) image & last (right-most ending) image...
# ...previous (left) image & next (right) image
def image_assignment(action, content_locator, gallery_map):
    # if there aren't any images available for the title, state it for debugging case.
    unavailable_image = "No image available"
    if (content_locator not in gallery_map) or (len(gallery_map[content_locator]) == 0):
        return unavailable_image
    
    # depending on button actions, shift index of image path within list to set for display.
    if action == "first":
        current_image[content_locator] = 0
    if action == "last":
        current_image[content_locator] = len(gallery_map[content_locator]) - 1
    if action == "previous":
        current_image[content_locator] -= 1
        if (current_image[content_locator] < 0):
            current_image[content_locator] = len(gallery_map[content_locator]) - 1 # loop around to the end image
    if action == "next":
        current_image[content_locator] += 1
        if (current_image[content_locator] >= len(gallery_map[content_locator])):
            current_image[content_locator] = 0  # loop back around to first image in list of the set

    display = gallery_map[content_locator][current_image[content_locator]]
    return display

def gallery_response(display):
    with open("txt/image_response.txt", "w") as f:
        f.write(display)

# continiously check request for new updates (also calling for all functions that were used)
while True:
    time.sleep(0.1)

    try:
        request, action, content_locator = gallery_request()
    except FileNotFoundError:
        continue

    # ignore empty requests or any unchanged requests
    if request == "" or request == previous_request:
        continue
    previous_request = request

    display = image_assignment(action, content_locator, gallery_map)
    gallery_response(display)

# ORDER OF OPPERATION FOR TESTING:
# 1. run this (and all the other ms) first
# 2. run flask (to connect codes to the live html website)
# 3. have at it!