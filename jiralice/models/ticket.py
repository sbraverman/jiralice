import os
import requests
import json
from requests.auth import HTTPBasicAuth
import logging

class Ticket(object):

    FIELDS_KEY = 'fields'
    PROJECT_KEY = 'project' 
    SUMMARY_KEY = 'summary'
    DESCRIPTION_KEY = 'description'
    ISSUE_TYPE_KEY = 'issuetype'
    LABELS_KEY = 'labels'

    A_JIRA_URL = os.environ['A_JIRA_URL']
    JIRA_PROJECT = os.environ['JIRA_PROJECT']
    CUSTOME_FIELDS = os.environ['CUSTOM_FIELDS']
    ISSUE_TYPE = os.environ['ISSUE_TYPE']
    LABELS = os.environ['LABELS']
    JIRA_USERNAME = os.environ['JIRA_USENAME']
    JIRA_PASSWORD = os.environ['JIRA_PASSWORD']


    def __init__(self, data):
        self.incident_number = self.get_incident_number(data)
        self.summary = self.get_summary(data)
        self.ticket_data = {self.FIELDS_KEY: {}}
        self.jira_auth = self.get_jira_auth()
        self.ticket_url = None
        self.pager_duty_link = self.get_pager_duty_link(data)
        self.set_ticket_data()

    def set_ticket_data(self):
        self.update_ticket(self.get_project_field())
        self.update_ticket(self.get_summary_field())
        self.update_ticket(self.get_description_field())
        self.update_ticket(self.get_issuetype_field())
        self.update_ticket(self.get_labels_field())
        self.set_custom_fields()

    def create(self):
        try:
            headers = {'Content-Type': 'application/json'}
            create_ticket_url = '{0}/rest/api/2/issue/'.format(self.JIRA_URL)
            request = requests.post(create_ticket_url, headers=headers, auth=self.jira_auth, data=json.dumps(self.ticket_data))
            # Printing below will help determine why ticket creation failed. e.g. "custom_fields" your ticket requires 
            print request.text
            self.ticket_url = request.json()['key']
        except Exception as e:
            raise BadRequestError('Error occurred while creating ticket', e)

    @classmethod
    def exists(cls, data):
        try:
            incident_number = cls.get_incident_number(data)
            jira_url = cls.JIRA_URL
            project = cls.JIRA_PROJECT
            search_ticket_url = "{0}/rest/api/2/search?jql=project={1}+and+text~'pagerduty+{2}'".format(jira_url, project, incident_number)
            request = requests.get(search_ticket_url, auth=cls.get_jira_auth())
            total_tickets = request.json()['total'] 
            if total_tickets > 0:
                logging.info('A ticket for incident #{0} already exists in JIRA'.format(incident_number))
                return True
            return False
        except Exception as e:
            logging.info('Failed to determine if ticket exists in JIRA. {0}'.format(e))
            return True
   
    def set_custom_fields(self):
        try:
            custom_fields = self.CUSTOM_FIELDS
            if custom_fields:
                for custom_field, value in custom_fields.iteritems():
                    self.update_ticket({custom_field: value})
        except Exception as e:
            raise BadRequestError('Could not set custom fields. Please refer to documentation', e)

    def get_issuetype_field(self):
        return {self.ISSUE_TYPE_KEY: {'name': self.ISSUE_TYPE}}

    def get_project_field(self):
        return {self.PROJECT_KEY: {'key': self.JIRA_PROJECT}}

    def get_labels_field(self): 
        return {self.LABELS_KEY: self.LABELS}

    def get_summary_field(self): 
        return {self.SUMMARY_KEY: "[PagerDuty] {0}: {1}".format(self.incident_number, self.summary)}

    def get_description_field(self): 
        return {self.DESCRIPTION_KEY: "*CURRENTLY*\nPagerDuty has triggered an alert\n{0}\n\n*PROBLEM*\n{1}\n\n*SOLUTION*\n* Investigate the alert.\n* Resolve the PagerDuty ticket\n* Create future tickets as necessary".format(self.pager_duty_link, self.summary)}

    def update_ticket(self, data):
        self.ticket_data[self.FIELDS_KEY].update(data)
             
    @classmethod
    def get_incident_number(cls, data):
        return data['incident']['incident_number'] 

    def get_summary(self, data):
        return data['incident']['trigger_summary_data']['subject']

    def get_pager_duty_link(self, data):
        return data['incident']['html_url'] 

    @classmethod
    def get_jira_auth(cls):
        return HTTPBasicAuth(cls.JIRA_USERNAME, cls.JIRA_PASSWORD)

