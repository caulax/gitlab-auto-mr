import yaml
import os
import requests
import json

class AutoMR():
    def __init__(self, filename):
        with open("./settings.yaml", "r") as credFile:
            self.credentians = yaml.load(credFile)
        self.creds = self.credentians['credentians']
        self.url = self.creds['url'] + "api/" + self.creds['api_version']
        self.headers = {'Private-Token': self.creds['private_token']}
        self.ass_id = self.creds['assignee_id']

        with open(filename, "r") as settingsFile:
            self.settings = yaml.load(settingsFile)
        self.labels = self.settings['global_labels']
        self.projects = self.settings['jobs_mr']
        
    def acceptMR(self):
        idOpenedMRAndIdProject = {}
        for project in self.projects:
            project_id = self.getIdProjectByPath(project["project"]["path"])
            if(project_id):
                idsMR = self.getIdOpenedMRByProjectIdAndLabels(project_id)
                if(idsMR):
                    for idMR in idsMR:
                        r = requests.put(self.url + "/projects/" + str(project_id) + "/merge_requests/" + str(idMR) + "/merge", headers=self.headers)
                        print("Merge project: " + project["project"]["path"] + " with label: " + self.labels + " returned: " + str(r))
                else:
                    print("No MR in project: " + project["project"]["path"] + " with label: " + self.labels)
            else:
                print("No project: " + project["project"]["path"])
    
    def createMR(self):
        for project in self.projects:
            project = project["project"]
            project_path =  project['path']
            source_branch = project['source_branch']
            target_branch = project['target_branch']
        
            project_id = self.getIdProjectByPath(project_path)
        
            if(project_id):           
                if(self.compareBranches(source_branch, target_branch, project_id)):
                    data = {'title' : project['title'],
                            'assignee_id' : self.ass_id,
                            'source_branch' : source_branch, 
                            'target_branch': target_branch, 
                            'labels': self.labels}     
                
                    r = requests.post(self.url + "/projects/" + str(project_id) + "/merge_requests", headers=self.headers, data=data)
                    print("Merge branches in project: " + project['path'] + " returned " + str(r))
                else:
                    print("No changes in project: " +  project['path'])
            else:
                print("No such project: " + project['path'])

    def getIdOpenedMRByProjectIdAndLabels(self, project_id):
        params = {'state' : 'opened',
                'labels': self.labels}
        r = requests.get(self.url + "/projects/" + str(project_id) + "/merge_requests", headers=self.headers, params=params)
        response = json.loads(r.text)
        if(response):
            idsMR = []
            for i in response:
                idsMR.append(i.get("iid"))
            return idsMR
        else:
            return None
            
    def getIdProjectByPath(self, project_path):
        project_path = project_path.replace("/", "%2F")
        r = requests.get(self.url + "/projects/" + project_path, headers=self.headers)
        response = json.loads(r.text)
        
        if(response.get("message") != None):
            return None
        else: 
            return response.get('id')

    def compareBranches(self, source_branch, target_branch, project_id):
        r = requests.get(self.url + "/projects/" + str(project_id) + "/repository/compare?from=" + target_branch + "&to=" + source_branch, headers=self.headers)
        response = json.loads(r.text)
        if(response.get('diffs')):
            return True
        else:
            return False
     
    def getSettings():
        pass
