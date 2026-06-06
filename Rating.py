import time

# The database which holds a rating for each title
rating_map = {
    "Nier Replicant" : 8.3,
    "Nier Automata" : 8.8,
    "Nier Reincarnation" : 7.1
}


def rating_request():
    content_data = {} # this stores the values that user have made & requested for

    with open("txt/rating_request.txt", "r") as f:
        request = f.read().strip()

    for line in request.splitlines():
        key, value = line.split("=")
        content_data[key] = value

    action = content_data.get("action") # get the event for action
    content_locator = content_data.get("title") # get the rating values for title

    return request, action, content_locator

previous_request = "" # to prevent repeatedly using the same request (avoid infinite loop)
with open("txt/rating_request.txt", "w") as f: # clear the current rating in rating_request.txt at every request (to disgard old ones)
    f.write("")

# depending on request (access page of a title or sort highest to lowest), return accordingly.
def rating_assignment(action, content_locator, rating_map):
    # if rating values not available for a title (not exist), state it (error: N/A or something),
    # otherwise return the rating values as a assigned value for that specific title (but as a str).
    unavailable_rating = "N/A"
    if action == "assigned_rating":
        if content_locator not in rating_map:
            return unavailable_rating
        else:
            return str(rating_map[content_locator])

    # if the users choose to sort titles by ratings (action execution -> highest-to-lowest),
    # loop through every pair of element and compare the rating index values.
    if action == "sorted_ratings":
        rankings = [] # list for keeping rack of sorted ratings (rankings)
        # set all as a list first (unsorted)...
        for title in rating_map:
            rankings.append([title, rating_map[title]])
        # ...then for every set of elements (title, rating) within the ranking list, sort it.   
        for i in range(len(rankings)):
            for j in range(len(rankings) - 1):
                # if current rating is higher than the next, swap their place and prioritize the higher values (bubble sort).
                if rankings[j][1] < rankings[j + 1][1]:
                    highest = rankings[j]
                    rankings[j] = rankings[j + 1]
                    rankings[j + 1] = highest

        result = ""     # what will be returned in response
        for topic in rankings:  # (ranking is now sorted, write result in response.)
            title = topic[0]
            rating = topic[1]
            result += title + "~" + str(rating) + "\n"
        return result   # (ex: Nier Automata~8.8 --> (next line) Nier Replicant~8.3 ...)
    else:
        return unavailable_rating 


def rating_response(ratings):
    # open and write in response.txt to send the ratings info back to main program.
    with open("txt/rating_response.txt", "w") as f:
        f.write(ratings)
        
# continously check request.txt for new updates
while True:
    time.sleep(0.1)

    try:
        request, action, content_locator = rating_request()
    except FileNotFoundError:
        continue

    # ignore empty requests or any unchanged requests
    if request == "" or request == previous_request:
        continue
    previous_request = request

    selection = rating_assignment(action, content_locator, rating_map)
    rating_response(selection)



