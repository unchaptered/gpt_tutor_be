from datetime import datetime


class DateProvider():

    def getCurrDatetimeStr(self) -> str:
        currDatetime = datetime.now()
        return currDatetime.strftime('%Y-%m-%d %H:%M:%S')
