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

import argparse
import config
import logging
import notify
import repository


def init():
    '''
    Initializes command line argument parser.
    Sets up logging environment.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", dest="verbose",
                        action="store_true", help="Enable DEBUG logging level.")
    parser.add_argument("-c", "--config", dest="config_file", default="config.json",
                        type=str, help="Path to the configuration file that is used.")
    parser.add_argument("-l", "--logfile", dest="log_file", default=None,
                        type=str, help="Path to the log file that is used.")
    params = parser.parse_args()

    if params.verbose:
        if params.log_file is None:
            logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)-8s] %(message)s")
        else:
            logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)-8s] %(message)s", filename=str(params.log_file))
    else:
        if params.log_file is None:
            logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)-8s] %(message)s")
        else:
            logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)-8s] %(message)s", filename=str(params.log_file))
    return params


def main(params):
    '''
    Main program. Loads the configuration, pulls the repositories and
    sends notification mails.
    '''
    logging.info("GitNotify - Push/Commit notification script")
    logging.info("(c) 2013 by Manuel Peuster <manuel@peuster.de>")

    c = config.Config.load_config(path=params.config_file)
    if c is None:
        logging.error("No configuration file loaded. Exiting.")
        exit(1)

    for repo_config in c["repositories"]:
        logging.info("Checking repository: %s (at: %s)", repo_config["name"], repo_config["url"])
        gr = repository.GitRepository(repo_config["name"], repo_config["url"])
        gr.clone()
        gr.pull()
        commit_list = gr.get_commits(branch=repo_config["branch"], limit=repo_config["limit"])
        ch = repository.CommitHistory()
        filtered_commit_list = ch.filter_commits_to_notify(commit_list)

        if len(filtered_commit_list) > 0:
            n = notify.Notifier(c, repo_config)
            if n.send_notifications(filtered_commit_list):
                ch.add_notified_commits(filtered_commit_list)
                logging.info("Notifications sent: %i", len(filtered_commit_list))
            else:
                logging.error("Error while sending notifications.")
        else:
            logging.info("No new commits. No notifications are generated.")


if __name__ == '__main__':
    params = init()
    main(params)
