#######################################################################
# This file is part of phil.
#
# Copyright (C) 2011, 2012, 2013 Will Kahn-Greene
#
# phil is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# phil is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with phil.  If not, see <http://www.gnu.org/licenses/>.
#######################################################################

import dateutil.rrule
from collections import namedtuple
import smtplib
import email.utils
from email.mime.text import MIMEText
#from tzlocal import get_localzone

FILE = 'file'
DIR = 'dir'










Config = namedtuple('Config', ['icsfile', 'remind', 'datadir', 'host',
                               'port', 'sender', 'to_list','username','password'])




Event = namedtuple('Event', ['event_id', 'rrule', 'summary', 'description','location'])


FREQ_MAP = {
    # TODO: Make sure this covers all of them.
    'HOURLY': dateutil.rrule.HOURLY,
    'DAILY': dateutil.rrule.DAILY,
    'MONTHLY': dateutil.rrule.MONTHLY,
    'YEARLY': dateutil.rrule.YEARLY,
    'WEEKLY':dateutil.rrule.WEEKLY    
}


WEEKDAY_MAP = {
    # TODO: Make sure this covers all of them.
    'SU': dateutil.rrule.SU,
    'MO': dateutil.rrule.MO,
    'TU': dateutil.rrule.TU,
    'WE': dateutil.rrule.WE,
    'TH': dateutil.rrule.TH,
    'FR': dateutil.rrule.FR,
    'SA': dateutil.rrule.SA
    }




def send_mail_smtp(sender, to_list, subject, body, host, port, username, password):
    print sender, to_list, subject, body, host, port, username, password
    sender_name, sender_addr = email.utils.parseaddr(sender)
    to_list = [email.utils.parseaddr(addr) for addr in to_list]

    for to_name, to_addr in to_list:
        msg = MIMEText(body,'text/html')
        msg['To'] = email.utils.formataddr((to_name, to_addr))
        msg['From'] = email.utils.formataddr((sender_name, sender_addr))
        msg['Subject'] = subject

    try:
        server = smtplib.SMTP(host, port)
        server.set_debuglevel(True)

        # identify ourselves, prompting server for supported features
        server.ehlo()

        # If we can encrypt this session, do it
        if server.has_extn('STARTTLS'):
            server.starttls()
            server.ehlo() # re-identify ourselves over TLS connection

            server.login(username, password)
            server.sendmail(sender_addr, [to_addr], msg.as_string())
    finally:
        server.quit()

