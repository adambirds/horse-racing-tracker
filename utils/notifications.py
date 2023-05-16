from datetime import datetime, timezone
import requests
import json

def send_discord_notification(meeting, race, ride, config_options):
    headers = {
        "Content-Type": "application/json"
    }

    formatted_date = datetime.strptime(meeting["date"], "%Y-%m-%d").strftime("%A %d %B %Y")

    with open("templates/horse-running.json", "r") as f:
        payload = json.load(f)
    
    payload['embeds'][0]['title'] = f"{ride['horse']} will run today in the {race['name']}:"
    payload['embeds'][0]['fields'][0]['value'] = meeting["course"]
    payload['embeds'][0]['fields'][1]['value'] = formatted_date
    payload['embeds'][0]['fields'][2]['value'] = race["time"]
    payload['embeds'][0]['fields'][3]['value'] = race["distance"]
    payload['embeds'][0]['fields'][4]['value'] = meeting["surface"]
    payload['embeds'][0]['fields'][5]['value'] = meeting["going"]
    payload['embeds'][0]['fields'][6]['value'] = ride["jockey"]
    payload['embeds'][0]['fields'][7]['value'] = ride["trainer"]
    payload['embeds'][0]['fields'][8]['value'] = ride["owner"]
    payload['embeds'][0]['fields'][9]['value'] = ride["age"]
    payload['embeds'][0]['fields'][10]['value'] = ride["sex"]
    if ride["last_ran_days"] != None:
        payload['embeds'][0]['fields'][11]['value'] = f'{ride["last_ran_days"]} days ago'
    else:
        payload['embeds'][0]['fields'][11]['value'] = "N/A"
    payload['embeds'][0]['fields'][12]['value'] = ride["form"]
    payload['embeds'][0]['fields'][13]['value'] = ride["current_odds"]
    payload['embeds'][0]['fields'][14]['value'] = ride["handicap"]
    payload['embeds'][0]['fields'][15]['value'] = ride["commentary"]

    payload['embeds'][0]['timestamp'] = datetime.now(tz=timezone.utc).isoformat()

    payload = json.dumps(payload, indent=4)

    response = requests.post(config_options["DISCORD_WEBHOOK_URL"], headers=headers, data=payload)
