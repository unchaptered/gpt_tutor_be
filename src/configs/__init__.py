import os
from setproctitle import setproctitle
from utilities.handler.scheduler_handler import SchHandler

setproctitle('AI_SERVER')

isServerReady = os.environ.get('RUN_MAIN', False)

if isServerReady:

    try:
        schHandler = SchHandler()
        schHandler.run()

    except Exception as e:
        print(e)
