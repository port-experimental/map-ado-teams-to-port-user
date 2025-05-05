# Map Azure DevOps Teams to Port Users
This is a python script to map ADO users to port users. 

Currently Port does not support appending entities to an array of entities i.e 1 to many relation. This script can be run as a once off or inside of a pipeline on a schedule.

The script will:
1. Authenticate to your Port organisation
2. Fetch your ADO Teams and Port users
3. For each Port User, iterate through the ADO Teams and map against their members
4. Patch the Port User entity via the API

This script has been tested with:
* Python 3.9.6
* PIP 21.2.4
* Requests 2.32.2

# Requirements
* Port ADO integration
* ADO Teams being ingested
* Port Client ID and Client Secret
* Relation property for Port User to ADO Teams blueprint
```
{
  "identifier": "_user",
  "description": "This blueprint is synced with active or invited Port users",
...
...
  "relations": {
    "azure_dev_ops_teams": {
      "title": "Azure DevOps Teams",
      "target": "azureDevopsTeam",
      "required": false,
      "many": true
    }
}
```

# Running the script
## Install requirements
```
pip install -r requirements.txt
```

## Required Environment Vars
```
export CLIENT_ID=<Port Client ID>
export CLIENT_SECRET=<Port Client Secret>
export BLUEPRINT_ID=<ADO Blueprint Name>
export RELATION_NAME=<Identifier of the ADO Teams relation property on the port user blueprint>
```

## Run the script
```
python main.py
```