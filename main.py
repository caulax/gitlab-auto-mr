import yaml
import os
import requests
import json

def main():
    creds = getSettings()['credentians']
    projects = getSettings()['jobs_mr']
    url = creds['url'] + "api/" + creds['api_version'] + "/projects/"
    headers = {'Private-Token': creds['private_token']}
    ass_id = creds['assignee_id']
    createNewMR(projects, url, headers, ass_id)

def createNewMR(projects, url, headers, ass_id):
    for project in projects:
        project = project["project"]
        project_path =  project['path'].replace("/", "%2F")
        source_branch = project['source_branch']
        target_branch = project['target_branch']

        project_id = getIdProjectByPath(project_path, url, headers)
        if(project_id):
            hash_source_branch = getHashOfLastCommitByBranch(source_branch, project_id, url, headers)
            hash_target_branch = getHashOfLastCommitByBranch(target_branch, project_id, url, headers)
            if(hash_source_branch and hash_target_branch):
                if(hash_source_branch != hash_target_branch):

                    data = {'title' : project['title'],
                            'assignee_id' : ass_id,
                            'source_branch' : source_branch, 
                            'target_branch': target_branch, 
                            'labels': project['labels']}     
                
                    r = requests.post(url + str(project_id) + "/merge_requests", headers=headers, data=data)
                    print("Merge branches on project " + project['path'] + " returned " + str(r))
                else:
                    print("Hash commits equals on project " + project['path'])
            else:
                print("Wrong branches name on project " +  project['path'])
        else:
            print("No such project: " + project['path'])

def getIdProjectByPath(path, url, headers):
    r = requests.get(url + path, headers=headers)
    response = json.loads(r.text)
    
    if(response.get("message") != None):
        return None
    else: 
        return response.get('id')

def getHashOfLastCommitByBranch(branch_name, project_id, url, headers):
    r = requests.get(url + str(project_id) + "/repository/commits/?ref_name=" + branch_name, headers=headers)
    response = json.loads(r.text)

    if not response:
        return None
    else: 
        return response[0].get('id')

       
def getSettings():
    with open("./settings.yaml", 'r') as ymlfile:
        return yaml.load(ymlfile)

if __name__ == '__main__':
    main()
