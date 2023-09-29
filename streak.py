class Streak():
    """holds statistical data for habits """
    def __init__(self):
       self.success_period = 0
       self.total_period = 0
       self.days_from_completion = None
       self.log = []
       
    def success_rate(self):
        try:
            self.success_period/self.total_period
        except ZeroDivisionError:
            pass