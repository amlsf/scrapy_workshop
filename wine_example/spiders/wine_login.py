# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import urllib
import urlparse
from netrc import netrc

from scrapy import Request
from scrapy.http.response.html import HtmlResponse
from scrapy.spider import Spider
import scrapy.log as _log


class AuthenticatedDrunkSpider(Spider):
    name = 'authed-wine-spider-L5'

    def start_requests(self):
        u = 'https://www.wine.com/v6/account/login.aspx'
        yield Request(u)

    def parse(self, response):
        """
        :type response: HtmlResponse
        """
        self.log('Welcome, <%s>' % response.url)
        url_parsed = urlparse.urlparse(response.url)
        netrc_hostname = url_parsed.hostname
        password, username = self._get_credentials(netrc_hostname)
        if username is None:
            raise ValueError('I require either a "USERNAME" in settings'
                             ' or a .netrc for %s' % netrc_hostname)
        if password is None:
            raise ValueError('I require either a "PASSWORD" in settings'
                             ' or a .netrc for %s' % netrc_hostname)

        post_fields = {}
        # <form name="aspnetForm" method="post" id="aspnetForm">
        aspnet_form = response.css('#aspnetForm')
        # grab all of ASP.net's hidden cruft
        for hidden in aspnet_form.css('input[type=hidden]'):
            i_name = ''.join(hidden.xpath('@name').extract())
            i_value = ''.join(hidden.xpath('@value').extract())
            post_fields[i_name] = i_value
        email_name = ''.join(aspnet_form.css('input[type=text][name$=Email]').xpath('@name').extract())
        post_fields[email_name] = username
        password_name = ''.join(aspnet_form.css('input[type=password]').xpath('@name').extract())
        post_fields[password_name] = password

        # <input type="submit" name="ctl00$BodyContent$Login$btnSubmit" value="Sign In"
        submit_value = 'Sign In'
        # careful, there is a dummy submit button, but its value is ""
        sign_ins = aspnet_form.css('input[type=submit][value="%s"]' % submit_value).xpath('@name').extract()
        assert len(sign_ins) == 1, 'Expected only one sign-in element'
        sign_in_name = sign_ins[0]
        post_fields[sign_in_name] = submit_value

        # ensure post keys are stable, to prevent map key ordering from blowing up tests
        body_keys = post_fields.keys()
        body_keys.sort()
        body = urllib.urlencode([(k, post_fields[k]) for k in body_keys])
        # self.log('POST %s\n%s' % (response.url, body))
        headers = {
            # it appears Scrapy does not send this by default;
            # presumably because it doesn't know *what* our body is
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        yield Request(response.url, self.check_login, method='POST', headers=headers, body=body)

    def check_login(self, response):
        self.log('Welcome, <%s>' % response.url)
        name = response.css('.profile[role=menu] > header::text').extract()
        if name:
            self.log('Logged-in Name = %s' % repr(name))
        else:
            self.log('EGAD, Login Failed!', level=_log.ERROR)

    def _get_credentials(self, hostname):
        """
        :param hostname: the hostname of the intended target; used for ``.netrc`` lookups
                        when the credentials are not in ``settings``
        :type hostname: str
        :return: a (username, password) tuple where ``username`` and ``password`` may be ``None``
                 but the tuple will not be
        :rtype: tuple(unicode, unicode)
        """
        username = None
        password = None
        nc = netrc()
        netrc_item = nc.authenticators(hostname)
        if netrc_item:
            #: :type: str
            usr = netrc_item[0]
            #: :type: str
            pword = netrc_item[2]
            if usr and pword:
                username = usr.decode('utf-8')
                password = pword.decode('utf-8')

        if not username:
            username = self.settings.get('USERNAME')
            if isinstance(username, str):
                username = username.decode('utf-8')
        if not password:
            password = self.settings.get('PASSWORD')
            if isinstance(password, str):
                password = password.decode('utf-8')
        return password, username
