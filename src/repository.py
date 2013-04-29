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

import git
import logging
import os
import time


class GitRepository(object):

    def __init__(self, repo_name, repo_remote_url, repo_base_path="/tmp"):
        self.repo_name = repo_name
        self.repo_remote_url = repo_remote_url
        self.repo_base_path = repo_base_path

    def __open_repository(self):
        try:
            logging.debug("Open repository: %s", self.repo_name)
            return git.Repo(self.repo_base_path + "/" + self.repo_name)
        except:
            logging.exception("Can not open repository: %s", self.repo_name)

    def clone(self):
        if not os.path.exists(self.repo_base_path + "/" + self.repo_name):
            try:
                logging.info("Cloning repository: %s", self.repo_remote_url)
                git.Repo.clone_from(self.repo_remote_url,
                                    self.repo_base_path + "/" + self.repo_name)
            except:
                logging.exception("Can not clone repository: %s",
                                  self.repo_remote_url)

    def pull(self):
        r = self.__open_repository()
        try:
            logging.info("Pull from repository: %s", self.repo_name)
            r.remotes.origin.pull()
        except AssertionError:
            pass
        except:
            logging.exception("Can not pull from repository: %s",
                              self.repo_name)

    def get_commits(self, branch="master", limit=20):
        # TODO: Add branch and limit to configuration
        r = self.__open_repository()
        result = []
        for c in r.iter_commits(branch, max_count=limit):
            result.append(GitCommit.create(c, self.repo_name))
        return result


class GitCommit(object):

    def __init__(self):
        self.repo_name = None
        self.hexsha = None
        self.author = None
        self.authored_date = None
        self.committer = None
        self.committed_date = None
        self.message = None

    def __repr__(self):
        return "Commit(%s:%s, %s, %s, %s, %s, %s)" % (self.repo_name,
                                                      self.hexsha,
                                                      self.author,
                                                      self.authored_date,
                                                      self.committer,
                                                      self.committed_date,
                                                      self.message)

    @staticmethod
    def create(source, repo_name):
        c = GitCommit()
        c.repo_name = repo_name
        c.hexsha = source.hexsha
        c.author = str(source.author)
        c.authored_date = time.strftime("%Y-%m-%d %H:%M",
                                        time.gmtime(source.authored_date))
        c.committer = str(source.committer)
        c.committed_date = time.strftime("%Y-%m-%d %H:%M",
                                         time.gmtime(source.committed_date))
        c.message = str(source.message)
        logging.debug("Created: " + str(c))
        return c


class CommitHistory(object):

    def __init__(self, path="history.dat"):
        self.commit_history = []
        self.path = path
        self.__load_from_file()

    def __load_from_file(self):
        try:
            logging.info("Loading commit history file: %s", self.path)
            f = open(self.path, "a+")
            f.seek(0, 0)
            for line in f:
                if ':' in line:
                    self.commit_history.append(line.strip())
            f.close()
        except:
            logging.exception("Can not open commit history file: %s",
                              self.path)

    def filter_commits_to_notify(self, commit_list):
        logging.info("Filtering commit list for not yet notified commits")
        result = []
        for c in commit_list:
            if not str("%s:%s" % (c.repo_name, c.hexsha)) \
                    in self.commit_history:
                result.append(c)
        return result

    def add_notified_commits(self, commit_list):
        try:
            logging.info("Updating commit history file: %s", self.path)
            f = open(self.path, "a")
            for c in commit_list:
                f.write(str("%s:%s\n" % (c.repo_name, c.hexsha)))
            f.close()
        except:
            logging.exception("Can not update commit history file: %s",
                              self.path)
