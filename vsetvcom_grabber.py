#!/usr/bin/env python
import argparse
import sys
import xmltv
from datetime import datetime, date, time, timedelta, timezone
from grab import Grab
from functools import partial
from transliterate import translit
from urllib.parse import urljoin


BASE_URL = "http://www.vsetv.com/"
EPG_URL = "schedule_package_personal_day_{}_nsc_1.html"
MAPPING = {
    "f0": "0",
    "d9": "1",
    "z0": "5"
}


parser = argparse.ArgumentParser(description="vsetv.com grabber.")
group = parser.add_mutually_exclusive_group()
parser.add_argument("-u", "--user", required=True, help="user")
parser.add_argument("-p", "--password", required=True, help="password")
parser.add_argument("-d", "--days", type=int, default=1, help="number of days")
parser.add_argument("-z", "--timezone", default=None, help="timezone")
group.add_argument("-o", "--output", default="tv_guide.xml", help="output file")
group.add_argument("--stdout", action="store_true", help="output to stdout")
args = parser.parse_args()


g = Grab()
g.setup(
    post={"inlogin": args.user, "inpassword": args.password},
    timeout=60000
)
g.go(urljoin(BASE_URL, "login.php"))
g.go(urljoin(BASE_URL, EPG_URL.format(date.today())))
channel_elems = g.doc.select(".//td[@class='channeltitle']").text_list()


def translit_channel(channel_name):
    channel_name = channel_name.lower().replace(" ", "_")
    return translit(channel_name, "ru", reversed=True)


def grab_pages():
    for day in reversed(range(args.days)):
        date_ = date.today() + timedelta(days=day)
        g.go(urljoin(BASE_URL, EPG_URL.format(date_)))
        main_selector = g.doc.select(".//div[@id='schedule_container']")
        amount_channels = range(len(main_selector))
        yield date_, main_selector, amount_channels


def get_channels_titles_dict():
    g.go(urljoin(BASE_URL, EPG_URL.format(date.today())))
    return (
        {"display-name": [(elem, u"ru")], "id": "{}_{}".format(translit_channel(elem), i)}
        for i, elem in enumerate(channel_elems, 1)
    )


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


def get_starttime(main_selector, amount_channels):
    return (
        list(map(
            deobfuscate_start_time,
            main_selector[i].select(
                "./div[@class='time' or @class='onair' or @class='pasttime']"
            ).selector_list
        )) for i in amount_channels
    )


def parse_start_time_string(start_time_string, date_=None):
    hour, minute = [int(string) for string in start_time_string.split(":")]
    return datetime.combine(date_, time(hour, minute))


def correct_starttime(date_, main_selector, amount_channels):
    starttime_lists = [
        list(map(partial(parse_start_time_string, date_=date_), p))
        for p in get_starttime(main_selector, amount_channels)
    ]
    for starttime in starttime_lists:
        for i, this_date in enumerate(starttime, 1):
            try:
                next_date = starttime[i]
                if this_date > next_date:
                    starttime[i] += timedelta(days=1)
            except IndexError:
                continue
    return starttime_lists


def get_stoptime(date_, start_time_lists, transitions):
    if not transitions:
        d = date_ + timedelta(days=1)
        t = time(5, 0)
        transitions = (datetime.combine(d, t) for i in start_time_lists)
    for transition, start_time_list in zip(transitions, start_time_lists):
        new_start_time = start_time_list[1:]
        new_start_time.append(transition)
        yield new_start_time


def get_programmes_titles(main_selector, amount_channels):
    return (
        main_selector[i]
        .select("./div[@class='prname2' or @class='pastprname2']")
        .text_list() for i in amount_channels
    )


def make_dict():
    transitions = []
    tz_part = "" if not args.timezone else " {}".format(args.timezone)
    for page in grab_pages():
        date_, main_selector, amount_channels = page
        titles = get_programmes_titles(main_selector, amount_channels)
        start_time_lists = correct_starttime(date_, main_selector, amount_channels)
        stop_time_lists = get_stoptime(date_, start_time_lists, transitions)
        iterable = zip(titles, start_time_lists, stop_time_lists, channel_elems)
        for index, (i, j, k, channel_elem) in enumerate(iterable, 1):
            for a, b, c in zip(i, j, k):
                yield {
                    "channel": "{}_{}".format(translit_channel(channel_elem), index),
                    "start": "{}{}".format(b.strftime("%Y%m%d%H%M%S"), tz_part),
                    "stop": "{}{}".format(c.strftime("%Y%m%d%H%M%S"), tz_part),
                    "title": [(a, u"ru")]
                }
        transitions = (starttime[0] for starttime in start_time_lists)


def write(file):
    w = xmltv.Writer()
    for i in get_channels_titles_dict():
        w.addChannel(i)
    for i in make_dict():
        w.addProgramme(i)
    els = w.root.getchildren()
    new_els = sorted(els, key=lambda el: (el.get("channel", ""), el.get("id", ""), el.get("start", "")))
    w.root[:] = new_els
    w.write(file, pretty_print=True)


if __name__ == "__main__":
    if args.stdout:
        write(sys.stdout.buffer)
    else:
        write(args.output)
