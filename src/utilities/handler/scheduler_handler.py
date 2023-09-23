from apscheduler.schedulers.background import BackgroundScheduler

# modules
from utilities.handler.work_handler import workHandler

class SchHandler():

    isInitialLoading: bool = False
    backScheduler: BackgroundScheduler

    def __init__(self):

        if self.isInitialLoading:
            return
        
        SCHEDULER_TERM = 15

        self.backScheduler = BackgroundScheduler({
            'apscheduler.job_defaults.max_instances': 1
        })
        self.backScheduler.add_job(
            workHandler.callGpt, 'interval', seconds=SCHEDULER_TERM)

        self.isInitialLoading = True

    def run(self):

        try:
            self.backScheduler.start()
        except Exception as e:
            self.backScheduler.shutdown()
