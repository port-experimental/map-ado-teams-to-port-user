import os
import requests
import json

# Load environment variables
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
blueprint_id = os.getenv("BLUEPRINT_ID")
relation_name = os.getenv("RELATION_NAME")
if not client_id or not client_secret:
    raise EnvironmentError(
        "client_id and client_secret must be set as environment variables."
    )


# Function to get JWT token
def get_jwt_token(client_id, client_secret):
    url = "https://api.getport.io/v1/auth/access_token"
    payload = {
        "clientId": client_id,
        "clientSecret": client_secret,
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    response = requests.post(url, data=json.dumps(payload), headers=headers)
    if response.status_code == 200:
        return response.json().get("accessToken")
    else:
        raise Exception(
            f"Failed to get JWT token: {response.status_code} {response.text}"
        )


# Function to get all entity information for a blueprint
def get_entities_for_blueprint(blueprint_id, jwt_token):
    url = f"https://api.getport.io/v1/blueprints/{blueprint_id}/entities"
    headers = {"Authorization": f"Bearer {jwt_token}"}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(
            f"Failed to get entities: {response.status_code} {response.text}"
        )


# get the Port user entities.
def get_user_entities(jwt_token):
    url = f"https://api.getport.io/v1/blueprints/_user/entities"
    headers = {"Authorization": f"Bearer {jwt_token}"}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(
            f"Failed to get entities: {response.status_code} {response.text}"
        )


# patch the user entities
def patch_user_entities(jwt_token, user_identifier, payload):
    url = f"https://api.port.io/v1/blueprints/_user/entities/{user_identifier}"
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json",
    }
    response = requests.patch(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(
            f"Failed to patch entity: {response.status_code} {response.text}"
        )


if __name__ == "__main__":
    # authenticate to Port's APIs using a JWT and grab the Port user and ADO team entities
    try:
        jwt_token = get_jwt_token(client_id, client_secret)
        ado_team_entities = get_entities_for_blueprint(blueprint_id, jwt_token)
        user_entities = get_user_entities(jwt_token)
    except Exception as e:
        print(f"Error: {e}")

    # map the ADO teams to the users and patch the entities via the API
    try:
        users_to_patch = []
        print("Begin matching users to ADO teams")
        for user in user_entities["entities"]:
            memberof = []
            name = user.get("identifier")

            # find user in the ADO team entities
            for team in ado_team_entities["entities"]:
                team_members = team["relations"]["members"]
                if user.get("identifier") in team_members:
                    memberof.append(team.get("identifier"))

            # build the entity payload
            user_entity = {
              "identifier": user.get("identifier"),
              "relations": {relation_name: memberof},
            }
            if len(memberof) > 0: # omits users with no ADO teams
                users_to_patch.append(user_entity)
        print("Matching complete.")

        for entity in users_to_patch:
            print(entity)
            patch_user_entities(jwt_token, entity["identifier"], entity)
    except Exception as e:
        print(f"Error: {e}")
