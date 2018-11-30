import yaml
import os
import requests
import json


class AutoMR(object):

    def __init__(self, filename, action):
        
        self.git_url = os.environ["AUTOMR_URL"]
        self.api_version = os.environ["AUTOMR_API_VERSION"]
        self.token = os.environ["AUTOMR_TOKEN"]
        self.ass_id = os.environ["AUTOMR_ASS_ID"]
        
        self.url = self.git_url + "api/" + self.api_version
        self.headers = {'Private-Token': self.token}

        with open(filename, "r") as settingsFile:
            self.settings = yaml.load(settingsFile)
        self.labels = self.settings['global']['labels']
        self.projects = self.settings['jobs_mr']

        if action == "new-tag":
            self.branch = self.settings['global']['tag']['branch']
            self.tag = self.settings['global']['tag']['version']
        
    def accept_mr(self):
        for project in self.projects:
            project_id = self.get_id_project_by_path(project["project"]["path"])
            if project_id:
                ids_mr = self.get_id_opened_mr_by_project_id_and_labels(project_id)
                if ids_mr:
                    for idMR in ids_mr:
                        r = requests.put(self.url + "/projects/" + str(project_id) + "/merge_requests/" + str(idMR) + "/merge", headers=self.headers)
                        print("Merge project: " + project["project"]["path"] + " with label: " + self.labels + " returned: " + str(r))
                else:
                    print("No MR in project: " + project["project"]["path"] + " with label: " + self.labels)
            else:
                print("No project: " + project["project"]["path"])

    def create_mr(self):
        for project in self.projects:
            project = project["project"]
            project_path = project['path']
            source_branch = project['source_branch']
            target_branch = project['target_branch']
        
            project_id = self.get_id_project_by_path(project_path)

            if project_id:
                if self.compare_branches(source_branch, target_branch, project_id):
                    data = {'title' : project['title'],
                            'assignee_id' : self.ass_id,
                            'source_branch' : source_branch, 
                            'target_branch': target_branch, 
                            'labels': self.labels}     
                
                    r = requests.post(self.url + "/projects/" + str(project_id) + "/merge_requests",
                                      headers=self.headers, data=data)
                    print("Merge branches in project: " + project['path'] + " returned " + str(r))
                else:
                    print("No changes in project: " + project['path'])
            else:
                print("No such project: " + project['path'])

    def get_id_opened_mr_by_project_id_and_labels(self, project_id):
        params = {'state': 'opened',
                  'labels': self.labels}
        r = requests.get(self.url + "/projects/" + str(project_id) + "/merge_requests",
                         headers=self.headers, params=params)
        response = json.loads(r.text)
        if response:
            ids_mr = []
            for i in response:
                ids_mr.append(i.get("iid"))
            return ids_mr
        else:
            return None

    def get_id_project_by_path(self, project_path):
        project_path = project_path.replace("/", "%2F")
        r = requests.get(self.url + "/projects/" + project_path, headers=self.headers)
        response = json.loads(r.text)

        if response.get("message"):
            return None
        else:
            return response.get('id')

    def compare_branches(self, source_branch, target_branch, project_id):
        r = requests.get(self.url + "/projects/" + str(project_id) + "/repository/compare?from=" + target_branch + "&to=" + source_branch, headers=self.headers)
        response = json.loads(r.text)
        if response.get('diffs'):
            return True
        else:
            return False

    def get_latest_tag_by_project_id(self, project_id):
        r = requests.get(self.url + "/projects/" + str(project_id) + "/repository/tags", headers=self.headers)
        try:
            response = json.loads(r.text)[0]
            return response.get("name")
        except:
            return False

    def get_latest_commit_by_project_id_and_branch(self, project_id, branch):
        r = requests.get(self.url + "/projects/" + str(project_id) + "/repository/branches/" + branch,
                         headers=self.headers)
        try:
            response = json.loads(r.text)
            return response.get("commit").get("id")
        except:
            return False

    def get_latest_commit_by_tag_name(self, project_id, tag_name):
        r = requests.get(self.url + "/projects/" + str(project_id) + "/repository/tags/" + tag_name,
                         headers=self.headers)
        try:
            response = json.loads(r.text)
            return response.get("commit").get("id")
        except:
            return False

    def create_tag(self):
        for project in self.projects:
            project = project["project"]
            project_path = project['path']
        
            project_id = self.get_id_project_by_path(project_path)
            if project_id:

                # latest_tag = self.get_latest_tag_by_project_id(project_id)
                latest_tag = self.get_tag_by_major_version(self.tag, project_id)
                if latest_tag:
                    ct = self.compareTags(latest_tag, self.tag)
                    if ct == -1 or ct == 0:

                        latest_project_commit = self.get_latest_commit_by_project_id_and_branch(project_id, self.branch)
                        latest_tag_commit = self.get_latest_commit_by_tag_name(project_id, latest_tag)
                        if latest_project_commit != latest_tag_commit:
                            tag = self.use_mask_for_increment_tag_version(latest_tag, "0.0.1")
                            self.query_create_tag(project_id, tag, project['path'])
                        else:
                            print("No changes by commits in project: " + project['path'])
                    if ct == 1:
                        self.query_create_tag(project_id, self.tag, project['path'])
                else:
                    self.query_create_tag(project_id, self.tag, project['path'])
            else:
                print("No such project: " + project['path'])

    def query_create_tag(self, project_id, tag, project_path):
        data = {
            'id': project_id,
            'tag_name': tag,
            'ref': self.branch
        }

        r = requests.post(self.url + "/projects/" + str(project_id) + "/repository/tags",
                          headers=self.headers, data=data)
        if r.status_code == 400:
            print("Tag " + tag + " in project: " + project_path + ":" + self.branch + " already exist. Status: " + str(r.status_code))
        else:
            print("Tag " + tag + " in project: " + project_path + ":" + self.branch + " created. Status: " + str(r.status_code))

    def use_mask_for_increment_tag_version(self, tag, tag_mask):
        tag_ = map(int, tag.split("."))
        tag_mask_ = map(int, tag_mask.split("."))
        
        mask_changes = []
        
        try:
            for idx, val in enumerate(tag_mask_):
                if val > 0:
                    mask_changes.append(idx)
                    mask_changes.append(val)

            if mask_changes[0] == 0:
                tag_[0] += mask_changes[1]
                tag_[1] = 0
                tag_[2] = 0
            if mask_changes[0] == 1:
                tag_[1] += mask_changes[1]
                tag_[2] = 0
            if mask_changes[0] == 2:
                tag_[2] += mask_changes[1]

            tag_ = map(str, tag_)

            tag = '.'.join(tag_)
            return tag 
        except:
            return False

    def compareTags(self, f_tag, s_tag):
        f_tag = map(int, f_tag.split("."))
        s_tag = map(int, s_tag.split("."))

        for i in range(0, len(f_tag)):
            if(f_tag[i] > s_tag[i]):
                return -1
            if(f_tag[i] < s_tag[i]):
                return 1
        return 0

    # return latest tag by major number in tag
    # example list on tags ["2.3.1","2.3.2", "3.7.2", "3.7.3", "3.7.4"]
    # input params 2.0.0
    # output will be "2.3.2"
    def get_tag_by_major_version(self, tag, project_id):
        tag = map(int, tag.split("."))

        r = requests.get(self.url + "/projects/" + str(project_id) + "/repository/tags", headers=self.headers)

        response = json.loads(r.text)
        tags = []
        for i in response:
            repo_tag = i.get("name")
            if int(repo_tag[0]) == int(tag[0]):
                
                tags.append(repo_tag)
        if tags:
            return tags[0]
        return False
