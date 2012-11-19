# -*- coding: utf-8 -*-

# Copyright (C) 2012 Romain Roffé
#
# This file is part of Todomanager
# 
# Todomanager is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# Todomanager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Todomanager; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import pickle
import os
from libtodomanager.todomanager import *

__all__ = ["PickleSerializer"]

class PickleSerializer:
    def __init__(self, filePath):
        self.filePath = filePath
    
    def load(self):
        try:
            srcFile = open(self.filePath, 'rb')
        except IOError:
            return (ErrorCode.kFailToOpenFile, TodoManager(serializer=self.filePath))

        todo = pickle.load(srcFile)
        srcFile.close()
        return (ErrorCode.kOk, todo)

    def save(self, todo):
        tmpPath = "%s.tmp" % self.filePath
        dumpFile = open(tmpPath, 'wb')
        if dumpFile == None:
            return ErrorCode.kFailToOpenFile

        pickle.dump(todo, dumpFile)
        dumpFile.close()
        os.rename(tmpPath, self.filePath)
