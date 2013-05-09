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
    '''
    Represents a git repository.
    Implements typical git functions like pull or clone.
    '''

    def __init__(self, repo_name, repo_remote_url, repo_base_path="/tmp"):
        '''
        Init with remote address etc.
        '''
        self.repo_name = repo_name
        self.repo_remote_url = repo_remote_url
        self.repo_base_path = repo_base_path

    def __open_repository(self):
        '''
        Returns a connection to the repository.
        '''
        try:
            logging.debug("Open repository: %s", self.repo_name)
            return git.Repo(self.repo_base_path + "/" + self.repo_name)
        except:
            logging.exception("Can not open repository: %s", self.repo_name)

    def clone(self):
        '''
        Clones a remote repository to the local machine.
        '''
        if not os.path.exists(self.repo_base_path + "/" + self.repo_name):
            try:
                logging.info("Cloning repository: %s", self.repo_remote_url)
                git.Repo.clone_from(self.repo_remote_url,
                                    self.repo_base_path + "/" + self.repo_name)
            except:
                logging.exception("Can not clone repository: %s",
                                  self.repo_remote_url)

    def pull(self):
        '''
        Pulls latest version from a remote repository.
        '''
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
        '''
        Returns a list of commits.
        List length defined by limit.
        '''
        # TODO: Add branch and limit to configuration
        r = self.__open_repository()
        result = []
        for c in r.iter_commits(branch, max_count=limit):
            result.append(GitCommit.create(c, self.repo_name))
        return result


class GitCommit(object):
    '''
    Represents a single git commit.
    Contains names, hashes, and commit message.
    '''

    def __init__(self):
        '''
        Init.
        '''
        self.repo_name = None
        self.hexsha = None
        self.author = None
        self.authored_date = None
        self.committer = None
        self.committed_date = None
        self.message = None

    def __repr__(self):
        '''
        Returns nice string version of commit.
        '''
        return "Commit(%s:%s, %s, %s, %s, %s, %s)" % (self.repo_name,
                                                      self.hexsha,
                                                      self.author,
                                                      self.authored_date,
                                                      self.committer,
                                                      self.committed_date,
                                                      self.message)

    @staticmethod
    def create(source, repo_name):
        '''
        Class function to create a new commit object from a result
        of the git library.
        '''
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
    '''
    Handles the already notified commits.
    '''

    def __init__(self, path="history.dat"):
        '''
        Init.
        '''
        self.commit_history = []
        self.path = path
        self.__load_from_file()

    def __load_from_file(self):
        '''
        Loads the commit history from a file.
        '''
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
        '''
        Removes all commits from commit list which are already in the 
        commit history file.
        '''
        logging.info("Filtering commit list for not yet notified commits")
        result = []
        for c in commit_list:
            if not str("%s:%s" % (c.repo_name, c.hexsha)) \
                    in self.commit_history:
                result.append(c)
        return result

    def add_notified_commits(self, commit_list):
        '''
        Add new commits to commit history file.
        '''
        try:
            logging.info("Updating commit history file: %s", self.path)
            f = open(self.path, "a")
            for c in commit_list:
                f.write(str("%s:%s\n" % (c.repo_name, c.hexsha)))
            f.close()
        except:
            logging.exception("Can not update commit history file: %s",
                              self.path)
