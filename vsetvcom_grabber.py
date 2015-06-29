#!/usr/bin/env python
import xmltv
import argparse
from grab import Grab
from datetime import datetime, date, time, timedelta


def parse_args():
    """Parse script parameters and return its values."""
    parser = argparse.ArgumentParser(description="vsetv.com grabber.")
    parser.add_argument("-u",
                        required=True,
                        help="user")
    parser.add_argument("-p",
                        required=True,
                        help="password")
    parser.add_argument("-o",
                        default="tv_guide.xml",
                        help="output file")
    args = parser.parse_args()
    return args.u, args.p, args.o

g = Grab()
g.setup(post={"inlogin": parse_args()[0], "inpassword": parse_args()[1]},
        timeout=60000)
g.go("http://www.vsetv.com/login.php")
g.go("http://www.vsetv.com/schedule_package_personal_day_%s_nsc_1.html" %
     date.today())
main_selector = g.doc.select("//div[@id=\"schedule_container\"]")
amount_channels = range(len(main_selector))


def get_channels_titles_dict():
    return [{"display-name": [(elem, u"ru")], "id": str(i)}
            for i, elem in enumerate(
            g.doc.select("//td[@class=\"channeltitle\"]").text_list(), 1)]


def get_starttime():
    return [main_selector[i].select(
            "./div[@class=\"time\" or @class=\"onair\" or @class=\"pasttime\"]")
            .text_list() for i in amount_channels]


def correct_starttime():    
    dt = lambda st: datetime.combine(date.today(), time(int(st.split(":")[0]),
                                                        int(st.split(":")[1])))
    starttime_lists = [list(map(dt, p)) for p in get_starttime()]
    for starttime in starttime_lists:
        for i, this_date in enumerate(starttime, 1):
            try:
                next_date = starttime[i]
                if this_date > next_date:
                    starttime[i] += timedelta(days=1)
            except IndexError:
                continue
    return starttime_lists


def get_stoptime():
    stoptime_lists = []
    t = time(5, 0)
    d = date.today() + timedelta(days=1)
    dt = datetime.combine(d, t)
    for i in correct_starttime():
        del i[0]
        i.append(dt)
        stoptime_lists.append(i)
    return stoptime_lists


def get_programmes_titles():
    return [main_selector[i]
            .select("./div[@class=\"prname2\" or @class=\"pastprname2\"]")
            .text_list() for i in amount_channels]


def make_dict():
    final_dict = []
    for n, (i, j, k) in enumerate(zip(get_programmes_titles(),
                                      correct_starttime(),
                                      get_stoptime()), 1):
        for a, b, c in zip(i, j, k):
            final_dict.append({"channel": str(n),
                               "start": b.strftime("%Y%m%d%H%M%S"),
                               "stop": c.strftime("%Y%m%d%H%M%S"),
                               "title": [(a, u"ru")]})
    return final_dict


def write(file):
    w = xmltv.Writer()
    for i in get_channels_titles_dict():
        w.addChannel(i)
    for i in make_dict():
        w.addProgramme(i)
    w.write(file)

if __name__ == "__main__":
    write(parse_args()[2])
