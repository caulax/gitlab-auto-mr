import yaml
import os
import requests
import json

def main():
    creds = getSettings()['credentians']
    projects = getSettings()['jobs_mr']
    url = creds['url'] + "api/" + creds['api_version'] + "/projects/"
    headers = {'Private-Token': creds['private_token']}
    createNewMR(projects, url, headers)

def createNewMR(projects, url, headers):
    for project in projects:
        project = project["project"]
        project_path =  project['path'].replace("/", "%2F")
        data = {'title' : project['title'],
                'source_branch' : project['source_branch'], 
                'target_branch': project['target_branch'], 
                'labels': project['labels']}
        
        project_id = getIdProjectByPath(project_path, url, headers)
        if(project_id):
            r = requests.post(url + str(project_id) + "/merge_requests", headers=headers, data=data)
            print("Project " + project['path'] + " returned " + str(r))
        else:
            print("No such project: " + project['path'])

def getIdProjectByPath(path, url, headers):
    r = requests.get(url + path, headers=headers)
    response = json.loads(r.text)
    
    if(response.get("message") != None):
        return None
    else: 
        return response.get('id')
       
def getSettings():
    with open("./settings.yaml", 'r') as ymlfile:
        return yaml.load(ymlfile)

if __name__ == '__main__':
    main()
