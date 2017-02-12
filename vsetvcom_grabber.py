#!/usr/bin/env python
import xmltv
import argparse
from grab import Grab
from datetime import datetime, date, time, timedelta


MAPPING = {
    "f0": "0",
    "d9": "1",
    "z0": "5"
}


def parse_args():
    """Parse script parameters and return its values."""
    parser = argparse.ArgumentParser(description="vsetv.com grabber.")
    group = parser.add_mutually_exclusive_group()
    parser.add_argument("-u", required=True, help="user")
    parser.add_argument("-p", required=True, help="password")
    group.add_argument("-o", default="tv_guide.xml", help="output file")
    group.add_argument("--stdout", action="store_true", help="output to stdout")
    args = parser.parse_args()
    return args.u, args.p, args.o, args.stdout


g = Grab()
g.setup(
    post={"inlogin": parse_args()[0], "inpassword": parse_args()[1]},
    timeout=60000
)
g.go("http://www.vsetv.com/login.php")
g.go("http://www.vsetv.com/schedule_package_personal_day_{}_nsc_1.html".format(date.today()))
main_selector = g.doc.select(".//div[@id=\"schedule_container\"]")
amount_channels = range(len(main_selector))


def get_channels_titles_dict():
    return [
        {"display-name": [(elem, u"ru")], "id": str(i)}
        for i, elem in enumerate(
            g.doc.select(".//td[@class=\"channeltitle\"]").text_list(), 1)
    ]


def deobfuscate_start_time(div):
    """Vsetv obfuscates start time string replacing some digits by
    by <a class="f0"> and so on.
    """
    selector_list = div.select("./a|text()")
    start_time_string = ""
    for selector in selector_list:
        if not selector.text():
            string_part = MAPPING[selector.attr("class")]
        else:
            string_part = selector.text()
        start_time_string += string_part
    return start_time_string


def get_starttime():
    return [
        list(map(
            deobfuscate_start_time,
            main_selector[i].select(
                "./div[@class=\"time\" or @class=\"onair\" or @class=\"pasttime\"]"
            ).selector_list
        )) for i in amount_channels
    ]


def parse_start_time_string(start_time_string):
    return datetime.combine(
        date.today(),
        time(
            int(start_time_string.split(":")[0]),
            int(start_time_string.split(":")[1])
        )
    )


def correct_starttime():
    starttime_lists = [list(map(parse_start_time_string, p)) for p in get_starttime()]
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
    return [
        main_selector[i]
        .select("./div[@class=\"prname2\" or @class=\"pastprname2\"]")
        .text_list() for i in amount_channels
    ]


def make_dict():
    final_dict = []
    for n, (i, j, k) in enumerate(zip(get_programmes_titles(),
                                      correct_starttime(),
                                      get_stoptime()), 1):
        for a, b, c in zip(i, j, k):
            final_dict.append({
                "channel": str(n),
                "start": b.strftime("%Y%m%d%H%M%S"),
                "stop": c.strftime("%Y%m%d%H%M%S"),
                "title": [(a, u"ru")]
            })
    return final_dict


def write(file):
    w = xmltv.Writer()
    for i in get_channels_titles_dict():
        w.addChannel(i)
    for i in make_dict():
        w.addProgramme(i)
    w.write(file)


if __name__ == "__main__":
    if parse_args()[3]:
        import sys
        if sys.version_info.major == 3:
            write(sys.stdout.buffer)
        elif sys.version_info.major == 2:
            write(sys.stdout)
    else:
        write(parse_args()[2])
