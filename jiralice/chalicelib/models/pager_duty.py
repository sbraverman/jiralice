

class PagerDuty(object):

    @staticmethod
    def is_triggered_alert(data):
        try:
            return data['incident']['status'] == 'triggered'
        except Exception as e:
            return False
