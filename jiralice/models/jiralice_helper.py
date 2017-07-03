from chalice import BadRequestError

#from ticket import Ticket
from pager_duty import PagerDuty


class JiraliceHelper(object):

    def __init__(self, params):
        self.params = params

    def create_ticket(self):
        messages = self.params['messages']
        for message in messages:
            try:
                message_data = message['data']
                if PagerDuty.is_triggered_alert(message_data): 
                    #ticket = Ticket(message_data)
                    ticket.create()
                    # TODO update_pager_duty_with_ticket_info()
            except Exception as e:
                logging.info(e)
                raise BadRequestError('Error occurred creating ticket')

