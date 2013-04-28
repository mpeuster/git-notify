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


import json
import logging


class Config(object):

    @staticmethod
    def load_config(path="config.json"):
        try:
            f = open(path, "r")
            config = json.load(f)
            f.close()
            logging.info("Configuration file loaded: %s", path)
            return config
        except:
            logging.exception("Can not open configuration file: %s",
                              path)
            return None
