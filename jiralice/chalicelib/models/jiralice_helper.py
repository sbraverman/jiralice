from chalice import BadRequestError
from sys import exit
import logging

from ticket import Ticket
from pager_duty import PagerDuty


class JiraliceHelper(object):

    def __init__(self, params, env_vars):
        self.params = params
        self.env_vars = env_vars
        self.incident_ids = []

    def create_ticket(self):
        try:
            messages = self.params['messages']
        except Exception as e:
            return {"error": "Invalid payload received: {0}".format(e)}
        if not messages or len(messages) < 0:
            return {'error': 'messages is not iterable'}
        for message in messages:
            try:
                message_data = message['data']
                incident_id = Ticket.get_incident_number(message_data)
                if incident_id in self.incident_ids:
                    continue
                self.incident_ids.append(incident_id)
                
                if PagerDuty.is_triggered_alert(message_data) and not Ticket.exists(message_data, self.env_vars):
                    ticket = Ticket(message_data, self.env_vars)
                    ticket.create()
                    # TODO update_pager_duty_with_ticket_info()
            except Exception as e:
                logging.info('{0}'.format(e))
                return {"error": "Ticket could not be created: {0}".format(e)}
        return True

