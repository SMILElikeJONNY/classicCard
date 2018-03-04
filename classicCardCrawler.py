import scrapy as sc
import datetime
import config.general as generalConfig
import json

now = datetime.datetime.now()


def generateEvent(day,time,componist, title, location):
    event = dict(day=day,time =time,componist=componist, title= title, location = location)
    return event

def lastDayOfMonth(any_day):
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)  # this will never fail
    return next_month - datetime.timedelta(days=next_month.day)

class bsiSpider(sc.Spider):
    name = "classicCard"

    #startpage to crawl
    start_urls = [
        'http://www.classiccard.de/de_DE/program']


    def parse(self, response):

        events = []

        #currentDay

        currentDay = datetime.datetime.now().day
        currentMonth = datetime.datetime.now().month

        #get all events
        allRows = response.xpath('//table[@class="calendarTable"]//child::tr')
        self.method_name(allRows, currentDay, events)

        #save to file
        eventsDict = dict(events=events)
        with open(generalConfig.eventsWeekFile,'w') as f:
            f.write(json.dumps(eventsDict))
            f.close()



    def method_name(self, allRows, currentDay, events):
        for row in allRows:
            contentList = []
            contentRow = row.xpath('child::td')
            for index, content in enumerate(contentRow):
                content = content.xpath('child::div//text()').extract()
                contentList.append(content)

                # check date
                if (index == 0):
                    # TODO right + 7 Days New Request to the next month and so on und events größer als 18 Uhr
                    dayWrongFormat = content[0].split('.')[0]
                    month = content[0].split('.')[1]
                    dayWrongFormat = list(dayWrongFormat)
                    if (dayWrongFormat[0] == '0'):
                        day = int(dayWrongFormat[1])
                    else:
                        day = int(''.join(dayWrongFormat))

                    if ((currentDay + 8) == day):
                        return

                    #lastDayOfMonth = lastDayOfMonth(datetime.date(now.year, now.month, 1))

                    #7 Tage gehen in neunen Monat und noch nicht eine Woche
                    if(day < currentDay and ((day-currentDay)< 7)):
                        #request to next month

                        pass
                    #1Woche voll
                    elif((currentDay + 8) == day):
                        return



                # get the content
                else:
                    event = contentList[0][0] + ': ' +  contentList[0][1] + '\n' +  '\n'.join(contentList[1])

                    '''
                    if (len(contentList[1]) == 2):

                        event = generateEvent(contentList[0][0], contentList[0][1], '-', contentList[1][0],
                                              contentList[1][1])
                    else:
                        if(len(contentList) == 1):
                            break
                        else:
                            event = generateEvent(contentList[0][0], contentList[0][1], contentList[1][0],
                                              contentList[1][1], contentList[1][2])

                    # print(event)'''
                    events.append(event)

            contentList = []