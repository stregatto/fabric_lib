import pycurl
import datetime
import secchia
from fabric.api import *
from fabric.utils import *
from fabric.contrib import *
from StringIO import StringIO
from urllib import urlencode


class Curl(object):

    def perform(self, url, post_data, username, password):
        buffer = StringIO()
        userpwd = "%s:%s" % (username, password)
        postfields = urlencode(post_data)
        c = pycurl.Curl()
        c.setopt(c.URL, url)
        c.setopt(c.POSTFIELDS, postfields)
        c.setopt(pycurl.HTTPAUTH, pycurl.HTTPAUTH_BASIC)
        c.setopt(pycurl.USERPWD, userpwd)
        c.setopt(c.WRITEDATA, buffer)
        c.setopt(c.FOLLOWLOCATION, True)
        # print('urlencode:' + str(url) + ' postfields:' + str(postfields) + ' user:' + userpwd)
        c.perform()
        response = buffer.getvalue()
        # print response
        c.close()
        return response


class Nagios(object):

    def __init__(self):
        self.password = os.environ.get('APPLICATION_NAGIOS_PASSWORD', None)
        self.username = os.environ.get('APPLICATION_NAGIOS_USER', None)
        self.server = os.environ.get('APPLICATION_NAGIOS_SERVER', None)
        self.domain = os.environ.get('APPLICATION_DOMAIN', None)
        self.uri = os.environ.get('APPLICATION_NAGIOS_URI', '/nagios/cgi-bin/cmd.cgi')
        self.url = 'http://' + self.server + self.uri
        return

    def _set_data_downtime_(self, host, start_time, end_time, what, domain=None):
        if domain:
            host = host + '.' + domain
        # change the cmd_typ if you need to stop also the server or not

        if what == 'host':
            cmd_typ = 55
        else:
            cmd_typ = 86
        # print('what: %s' % what)
        # print('cmd_typ: %s' % cmd_typ)
        data = {'cmd_typ': int(cmd_typ),
                'cmd_mod': 2,
                'host': host,
                'com_data': 'Updating+application',
                'trigger': 0,
                'start_time': start_time,
                'end_time': end_time,
                'fixed': 1,
                'hours': 2,
                'minutes': 0,
                'btnSubmit': 'Commit'
                }
        return data

    def _set_data_check_(self, host, start_time, domain=None):
        if domain:
            host = host + '.' + domain
        # change the cmd_typ if you need to stop also the server or not
        data = {'cmd_typ': 96,
                'cmd_mod': 2,
                'host': host,
                'com_data': 'Updating+application',
                'trigger': 0,
                'start_time': start_time,
                'force_check': 1
                }
        return data

    def _check_error_(self, response):
        ERROR = 'Sorry, but you are not authorized to commit the specified command'
        if ERROR not in response:
            return True
        else:
            return False

    def check_host(self, host, start_time):
        data = self._set_data_check_(host, start_time)
        curl = Curl()
        response = curl.perform(self.url, data, self.username, self.password)
        if self._check_error_(response):
            check = True
        else:
            data = self._set_data_check_(host, start_time, self.domain)
            curl = Curl()
            response = curl.perform(self.url, data, self.username, self.password)
            if self._check_error_(response):
                check = True
            else:
                check = False
        if check:
            print('OK: Check forced for %s' % host)
        else:
            print('ERROR: Check problem for %s' % host)

    def set_downtime(self, host, start_time, end_time, what):
        if what == 'host' or what == 'services':
            self._set_downtime_(host, start_time, end_time, what)
        elif what == 'both':
            self._set_downtime_(host, start_time, end_time, 'services')
            self._set_downtime_(host, start_time, end_time, 'host')
        else:
            print('ERROR: No what is specified for %s' % host)

    def set_relative_downtime(self, host, downtime, what='both'):
        now = datetime.datetime.now()
        end_time = secchia.chop_seconds_microseconds(secchia.add_minutes(now,
                                                                         downtime))
        end_time = str(end_time)
        start_time = str(secchia.chop_seconds_microseconds(now))
        self.set_downtime(host, start_time, end_time, what)

    def _set_downtime_(self, host, start_time, end_time, what):
        data = self._set_data_downtime_(host, start_time, end_time, what)
        curl = Curl()
        response = curl.perform(self.url, data, self.username, self.password)
        if self._check_error_(response):
            set_downtime = True
        else:
            # I'm trying with the fqdn, because I'm not sure about the name of server
            if self.domain == '':
                print('WARNING: domain is emplty, set APPLICATION_DOMAIN var')
            data = self._set_data_downtime_(host, start_time, end_time, what, self.domain)
            response = curl.perform(self.url, data, self.username, self.password)
            if self._check_error_(response):
                set_downtime = True
            else:
                set_downtime = False
        if set_downtime:
            print('OK: Downtime for %s on %s' % (what, host))
        else:
            print('ERROR: Downtime not set for %s %s' % (what, host))


# export APPLICATION_NAGIOS_PASSWORD='inUsipb910'
# export APPLICATION_NAGIOS_USER='nagiosadmin'
# export APPLICATION_NAGIOS_SERVER='10.10.2.32'

# curl --silent --show-error -d "cmd_mod=2&cmd_typ=86&host=$HOST${SERVERS[$i]}.bravofly.intra&start_time=$STARTDATE&end_time=$ENDDATE&fixed=1&com_data=Updating+application"  "http://10.10.2.32/nagios/cgi-bin/cmd.cgi" -u "$USER:$PWD" |egrep  -i "infoMessage|errorMessage|connect"
