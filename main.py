import requests
import datetime
import os
import yaml

current_date = datetime.datetime.now().strftime("%Y-%m-%d")

API_URL = f"https://www.sportinglife.com/api/horse-racing/racing/racecards/{current_date}"
RACE_URL = "https://www.sportinglife.com/api/horse-racing/race/{}?includeVideos=true"

with open(
    os.path.join(
        os.path.dirname(__file__),
        "config.yaml"
    ),
    "r"
) as config_file:
    config = yaml.safe_load(config_file)

HORSES_TO_WATCH = config["horses_to_watch"]

HORSE_SEXES = (
    ("c", "Colt"),
    ("f", "Filly"),
    ("g", "Gelding"),
    ("m", "Mare"),
)

def main():
    response = requests.get(API_URL)
    
    meetings = []

    for meeting in response.json():
        if meeting["meeting_summary"]["course"]["country"]["long_name"] == "England" or meeting["meeting_summary"]["course"]["country"]["long_name"] == "Eire":
            meeting_object = {
                "course": meeting["meeting_summary"]["course"]["name"],
                "date": meeting["meeting_summary"]["date"],
                "country": meeting["meeting_summary"]["course"]["country"]["long_name"],
                "going": meeting["meeting_summary"]["going"],
                "surface": meeting["meeting_summary"]["surface_summary"],
                "races": []
            }

            for race in meeting["races"]:
                race_object = {
                    "id": race["race_summary_reference"]["id"],
                    "name": race["name"],
                    "distance": race["distance"],
                    "date": race["date"],
                    "time": race["time"],
                    "ride_count": race["ride_count"],
                    "has_handicap": race["has_handicap"],
                    "age": race["age"],
                    "race_class": race["race_class"],
                    "rides": []
                }

                race_response = requests.get(RACE_URL.format(race_object["id"]))
                race_response_json = race_response.json()

                for ride in race_response_json["rides"]:
                    ## Check if last_ran_days dict key exists
                    if "last_ran_days" in ride["horse"]:
                        last_ran_days = ride["horse"]["last_ran_days"]
                    else:
                        last_ran_days = None
                    
                    ## Check if horse has draw_number
                    if "draw_number" in ride:
                        draw_number = ride["draw_number"]
                    else:
                        draw_number = None
                    
                    ## Check if commentary exists
                    if "commentary" in ride:
                        commentary = ride["commentary"]
                    else:
                        commentary = None

                    ride_object = {
                        "horse": ride["horse"]["name"],
                        "jockey": ride["jockey"]["name"],
                        "trainer": ride["trainer"]["name"],
                        "owner": ride["owner"]["name"],
                        "age": ride["horse"]["age"],
                        "form": ride["horse"]["formsummary"]["display_text"],
                        "sex": dict(HORSE_SEXES).get(ride["horse"]["sex"]["type"]),
                        "last_ran_days": last_ran_days,
                        "draw_number": draw_number,
                        "cloth_number": ride["cloth_number"],
                        "handicap": ride["handicap"],
                        "favourite": ride["betting"]["favourite"],
                        "current_odds": ride["betting"]["current_odds"],
                        "commentary": commentary,
                    }
                
                    race_object["rides"].append(ride_object)

                meeting_object["races"].append(race_object)
            
            meetings.append(meeting_object)
    
    for horse in HORSES_TO_WATCH:
        ## Loop through meetings and check if horse is running in a race. If so, tell me what race, what time, and what course, form and odds and jockey.
        for meeting in meetings:
            for race in meeting["races"]:
                for ride in race["rides"]:
                    if ride["horse"] == horse:
                        formatted_date = datetime.datetime.strptime(meeting["date"], "%Y-%m-%d").strftime("%A %d %B %Y")

                        print(f'{horse} is running at {meeting["course"]}, on {formatted_date} at {race["time"]}, ridden by {ride["jockey"]}, trained by {ride["trainer"]}.')
                        print(f'The race is over {race["distance"]} on the {meeting["surface"]}, and the going is {meeting["going"]}.')
                        print(f'The horse is a {ride["age"]} year old {ride["sex"]}.')
                        print(f'Form: {ride["form"]}')
                        print(f'Odds: {ride["current_odds"]} ')
                        print(f'Commentary: {ride["commentary"]}')
                        if ride["last_ran_days"] != None:
                            print(f'Last ran: {ride["last_ran_days"]} days ago.')



if __name__ == "__main__":
    main()