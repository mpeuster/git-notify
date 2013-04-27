"""
    GitNotify - Push/Commit notification script

    Copyright (C) 2013 Manuel Peuster <manuel@peuster.de>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


class MailServer(object):

    def __init__(self, url, user, password):
        pass

    def send(self, mail):
        pass


class Mail(object):

    def __init__(self, mail_to, mail_from, mail_subject, mail_body):
        pass


class Notifier(object):

    def __init__(self):
        pass

    def send_notifications(self, commit_list):
        pass
