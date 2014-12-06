#!/usr/bin/env python
import xmltv
from grab import Grab
from datetime import datetime, date, time, timedelta
 
class VsetvGrabber:
    """Grabber for vsetv.com"""
    def __init__(self):      
        self.g = Grab()
        self.g.setup(cookies={"cll":"your_cookie", "cp":"your_cookie"})
        self.g.go('http://www.vsetv.com/schedule_package_personal_day_' + str(date.today()) + '_nsc_1.html')    
        self.amount_channels = len(self.g.doc.select('//div[@id="schedule_container"]'))
        self.main_selector = self.g.doc.select('//div[@id="schedule_container"]')
        
    def get_channels_titles_dict(self):
        return [{'display-name': [(elem, u'ru')], 'id': str(i+1)} for i,elem in enumerate(self.g.doc.select('//td[@class="channeltitle"]').text_list())]
     
    def get_starttime(self):
        return [self.main_selector[i].select('./div[@class="time" or @class="onair" or @class="pasttime"]').text_list() for i in range(self.amount_channels)]
     
    def convert_date(self, start_time):
        dt = str(date.today()) + " " + str(start_time)
        dt = datetime.strptime(dt, "%Y-%m-%d %H:%M")
        return dt
     
    def make_date(self):
        return [map(lambda x: self.convert_date(x), p) for p in self.get_starttime()]
     
    def correct_starttime(self):
        wrong_datetime = self.make_date()
        for nested_datetime_stack in wrong_datetime:
            for idx, this_date in enumerate(nested_datetime_stack):
                if ((idx + 1) != len(nested_datetime_stack)):
                    next_date = nested_datetime_stack[(idx + 1) % len(nested_datetime_stack)]
                    if this_date > next_date:
                        nested_datetime_stack[(idx + 1) % len(nested_datetime_stack)] += timedelta(days=1)
        return wrong_datetime
     
    def get_stoptime(self):
        new_time = []
        t = time(5, 0)
        d = date.today() + timedelta(days=1)
        dt = datetime.combine(d, t)
        for i in self.correct_starttime():
            i[1:].append(dt)
            new_time.append(i)
        return new_time
     
    def get_programmes_titles(self):
        return [self.main_selector[i].select('./div[@class="prname2" or @class="pastprname2"]').text_list() for i in range(self.amount_channels)]
     
    def time_to_string(self, datetime_object):
        return datetime_object.strftime("%Y%m%d%H%M%S")
     
    def make_dict(self):
        final_dict = []
        m = 1
        for i, j, k in zip(self.get_programmes_titles(), self.correct_starttime(), self.get_stoptime()):
            for a, b, c  in zip(i, j, k):
                final_dict.append({'channel': str(m), 'start': self.time_to_string(b), 'stop': self.time_to_string(c), 'title': [(a, u'ru')]})
            m += 1
        return final_dict
 
    def write(self, file):
        w = xmltv.Writer()
        for i in self.get_channels_titles_dict():
            w.addChannel(i)
        for i in self.make_dict():
            w.addProgramme(i)
        w.write(file)
        
if __name__ == '__main__':
    x = VsetvGrabber()
    x.write('tv_guide.xml')