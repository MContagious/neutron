#!/usr/bin/env python
# -*- coding: ISO-8859-15 -*-

#  Neutron plugin
#  plugin.py

#  Copyright (C) 2002-2006 Mike Mintz <mikemintz@gmail.com>
#  Copyright (C) 2007 Mike Mintz <mikemintz@gmail.com>
#                     Ana�l Verrier <elghinn@free.fr>

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

from config import Config
from logging import getLogger
from os import access as os_access, F_OK
from xmpp import NodeProcessed

class Plugin:
    logger = getLogger('plugin')
    
    def __init__(self):
        pass

    def plugin(self, cls, conn):
        cls.conn = conn
        cls.config = Config()
        cls.initialize_file = self.initialize_file
        cls.read_file = self.read_file
        cls.write_file = self.write_file
        cls.logger = getLogger('plugin.%s' % str(cls).split('.')[1])
        cls.NodeProcessed = NodeProcessed
        obj = cls()
        if obj.__dict__.has_key(self.__class__.__name__):
            Plugin.logger.error('Plugin %s v%s already plugged' % \
                                (obj.name, obj.version))
            raise
        obj.__dict__[self.__class__.__name__] = self
        for key in ('description', 'homepageurl', 'updateurl'):
            if obj.__dict__.has_key(key):
                continue
            obj.__dict__[key] = None
        for key, nb_args in [['post_connection', 1],
                             ['post_deconnection', 1],
                             ['message', 4],
                             ['outgoing_message', 3],
                             ['join', 3],
                             ['part', 3],
                             ['iq', 2],
                             ['presence', 2],
                             ['groupchat_invite', 7],
                             ['groupchat_decline', 4],
                             ['groupchat_config', 4]]:
            key_handlers = '%s_handlers' % key
            if (obj.__dict__.has_key(key_handlers) and
                obj.__dict__[key_handlers]):
                for handler in obj.__dict__[key_handlers]:
                    if handler.func_code.co_argcount != nb_args:
                        Plugin.logger.error('Plugin %s v%s : handler %s doesn\'t have %s arguments !' % (obj.name, obj.version, handler.func_code.co_name, nb_args))
                        raise
                conn.handlers[key].extend(obj.__dict__[key_handlers])
        if obj.__dict__.has_key('command_handlers') and \
               obj.__dict__['command_handlers']:
            for handler, command, access, description, syntax, examples in \
                    obj.__dict__['command_handlers']:
                if handler.func_code.co_argcount != 4:
                    Plugin.logger.error(
                        'Plugin %s v%s : handler %s doesn\'t have 4 arguments !'
                        % (obj.name, obj.version, handler.func_code.co_name))
                    raise
                conn.__dict__['command_handlers'][command] = {
                    'handler' : handler,
                    'access' : access,
                    'description' : description,
                    'syntax' : syntax,
                    'examples' : examples}
        return obj

    def initialize_file(self, filename, data=''):
        if not os_access(filename, F_OK):
            file_ = file(filename, 'w')
            if data:
                file_.write(data)
            file_.close()

    def read_file(self, filename):
        file_ = file(filename)
        data = file_.read()
        file_.close
        return data

    def write_file(self, filename, data):
        file_ = file(filename, 'w')
        file_.write(data)
        file_.close()

