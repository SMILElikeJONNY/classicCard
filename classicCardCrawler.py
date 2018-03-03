import scrapy as sc
import datetime
import config.general as generalConfig
import json

def generateEvent(day,time,componist, title, location):
    event = dict(day=day,time =time,componist=componist, title= title, location = location)
    return event

class bsiSpider(sc.Spider):
    name = "classicCard"

    #startpage to crawl
    start_urls = [
        'http://www.classiccard.de/de_DE/program']


    def parse(self, response):

        events = []

        #currentDay
        currentDay = datetime.datetime.now().day

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
                    dayWrongFormat = list(dayWrongFormat)
                    if (dayWrongFormat[0] == '0'):
                        day = int(dayWrongFormat[1])
                    else:
                        day = int(''.join(dayWrongFormat))

                    if ((currentDay + 8) == day):
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