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


import datetime
import logging
import smtplib


class MailServer(object):
    '''
    Represents an SMTP mail server.
    '''

    def __init__(self, url, port, user, password):
        '''
        Creates a SMTP server connection. Using the
        provided credentials.
        '''
        try:
            self.smtp = smtplib.SMTP(url, port=int(port))
            self.smtp.login(user, password)
            logging.info("Connection to SMTP server established: %s", url)
        except:
            logging.exception("Error while connecting to SMTP server.")
            self.smtp = None

    def send(self, mail):
        '''
        Sends the provided mail object.
        '''
        if self.smtp is None:
            return False
        try:
            self.smtp.sendmail(mail.mail_from, mail.mail_to, str(mail))
        except:
            logging.exception("Error while sending mail.")
            return False
        return True

    def quit(self):
        self.smtp.quit()


class Mail(object):
    '''
    Represents a mail.
    '''

    def __init__(self, mail_to, mail_from, mail_subject, mail_body):
        '''
        Creates a new mail.
        Gets sender, receiver, subject and content.
        '''
        self.mail_to = mail_to
        self.mail_from = mail_from
        self.mail_subject = mail_subject
        self.mail_body = mail_body
        self.mail_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    def __repr__(self):
        '''
        Returns mail in nice format.
        '''
        return "From: %s\nTo: %s\nSubject: %s\nDate: %s\n\n%s" \
            % (self.mail_from, self.mail_to, self.mail_subject, self.mail_date, self.mail_body)

    @staticmethod
    def generate(commit, repo_config, mail_from):
        '''
        Generates mail content from commit.
        '''
        subject = "GitNotify: %s committed to repository: %s" % (commit.committer, commit.repo_name)
        body = "New commit to repository: %s\n\n SHA: %s\nAuthor: %s\nAuthoredDate: %s\nCommitter: %s\nCommitedDate: %s\n\nMessage:\n%s\n" \
            % (commit.repo_name, commit.hexsha, commit.author, commit.authored_date, commit.committer, commit.committed_date, commit.message)

        mails = []
        for reciver in repo_config["mail_addresses"]:
            mails.append(Mail(reciver, mail_from, subject, body))
        return mails


class Notifier(object):
    '''
    Notification controller.
    '''

    def __init__(self, config, repo_config):
        '''
        Init.
        '''
        self.config = config
        self.repo_config = repo_config

    def send_notifications(self, commit_list):
        '''
        Sends a notification for each commit in commmit_list.
        '''
        ms = MailServer(self.config["smtp_server"],
                        self.config["smtp_port"],
                        self.config["smtp_user"],
                        self.config["smtp_password"])

        for commit in commit_list:
            mails = Mail.generate(commit, self.repo_config, self.config["mail_sender"])
            for m in mails:
                if not ms.send(m):
                    return False

        ms.quit()
        return True
