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


import logging
import repository


def main():
    logging.basicConfig(level=logging.DEBUG)

    logging.info("GitNotify v.0.1")

    repo_name = "Test"
    repo_rmote_url = "git@github.com:mpeuster/test.git"
    gr = repository.GitRepository(repo_name, repo_rmote_url)
    gr.clone()
    gr.pull()
    print gr.get_commits()

if __name__ == '__main__':
    main()
