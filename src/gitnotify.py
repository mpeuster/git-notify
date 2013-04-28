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
import repository


def init():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", dest="verbose",
                        action="store_true", help="Enable DEBUG logging level.")
    parser.add_argument("-c", "--config", dest="config_file", default="config.json",
                        type=str, help="Path to the configuration file that is used.")
    params = parser.parse_args()

    if params.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    return params


def main(params):
    logging.info("GitNotify v.0.1")

    c = config.Config.load_config(path=params.config_file)
    if c is None:
        exit(1)

    repo_name = c["repositories"][0]["name"]
    repo_rmote_url = c["repositories"][0]["url"]

    # TODO: Call the following lines for each repository
    gr = repository.GitRepository(repo_name, repo_rmote_url)
    gr.clone()
    #gr.pull()
    commit_list = gr.get_commits()
    ch = repository.CommitHistory()
    filtered_commit_list = ch.filter_commits_to_notify(commit_list)

    if len(filtered_commit_list) > 0:
        pass
        # TODO: Call notifier here
        #ch.add_notified_commits(filtered_commit_list)
    else:
        logging.info("No new commits. No notifications will be send.")


if __name__ == '__main__':
    params = init()
    main(params)
