# -*- coding: utf-8  -*-
#
# Copyright (C) 2009-2012 Ben Kurtovic <ben.kurtovic@verizon.net>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from datetime import datetime
from math import floor
from time import time

try:
    import pytz
except ImportError:
    pytz = None

from earwigbot.commands import Command

class Time(Command):
    """Report the current time in any timezone (UTC default), or in beats."""
    name = "time"
    commands = ["time", "beats", "swatch"]

    def process(self, data):
        if data.command in ["beats", "swatch"]:
            self.do_beats(data)
            return
        if data.args:
            timezone = data.args[0]
        else:
            timezone = "UTC"
        if timezone in ["beats", "swatch"]:
            self.do_beats(data)
        else:
            self.do_time(data, timezone)

    def do_beats(self, data):
        beats = ((time() + 3600) % 86400) / 86.4
        beats = int(floor(beats))
        self.reply(data, "@{0:0>3}".format(beats))

    def do_time(self, data, timezone):
        if not pytz:
            msg = "this command requires the 'pytz' module: http://pytz.sourceforge.net/"
            self.reply(data, msg)
            return
        try:
            tzinfo = pytz.timezone(timezone)
        except pytz.exceptions.UnknownTimeZoneError:
            self.reply(data, "unknown timezone: {0}.".format(timezone))
            return
        now = pytz.utc.localize(datetime.utcnow()).astimezone(tzinfo)
        self.reply(data, now.strftime("%Y-%m-%d %H:%M:%S %Z"))
