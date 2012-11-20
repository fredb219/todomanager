#! /usr/bin/env python
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

import unittest
from libtodomanager.todomanager import *
from todomanagercli.commands import *
from todomanagercli.shell import *

class TestPrintTagList(unittest.TestCase):
    def setUp(self):
        self.todo = TodoManager()
        self.cmd  = CommandPrintTagList() 

    def runTest(self):
        cmdParam = HandlerParam()
        cmdParamCount = 0

        res = self.cmd.runCommand(self.todo, cmdParamCount, cmdParam)
        self.assertEqual(res, CommandError.kOk)

class TestAddTag(unittest.TestCase):
    def setUp(self):
        self.todo = TodoManager()
        self.cmd  = CommandAddTag() 

    def runTest(self):
        cmdParam = HandlerParam()
        setattr(cmdParam, "name", "Tag1")
        cmdParamCount = 1

        self.assertEqual(self.todo.getTagCount(), 0)
        res = self.cmd.runCommand(self.todo, cmdParamCount, cmdParam)
        self.assertEqual(res, CommandError.kOk)
        self.assertEqual(self.todo.getTagCount(), 1)

        res = self.cmd.runCommand(self.todo, cmdParamCount, cmdParam)
        self.assertEqual(res, CommandError.kError)
        self.assertEqual(self.todo.getTagCount(), 1)

        cmdParam = HandlerParam()
        setattr(cmdParam, "name", "Tag2")
        res = self.cmd.runCommand(self.todo, cmdParamCount, cmdParam)
        self.assertEqual(res, CommandError.kOk)
        
        self.assertEqual(self.todo.getTagCount(), 2)
        res = self.todo.getTagByName("Tag1")
        self.assertNotEqual(res, None)
        res = self.todo.getTagByName("Tag2")
        self.assertNotEqual(res, None)

class TestPrintOpenedTicketList(unittest.TestCase):
    def setUp(self):
        self.todo = TodoManager()
        self.cmd  = CommandPrintOpenedTicketList() 

    def runTest(self):
        cmdParam = HandlerParam()
        cmdParamCount = 0

        res = self.cmd.runCommand(self.todo, cmdParamCount, cmdParam)
        self.assertEqual(res, CommandError.kOk)

class TestOpenTicket(unittest.TestCase):
    def setUp(self):
        self.todo = TodoManager()
        self.cmd  = CommandOpenTicket() 

    def runTest(self):
        cmdParam = HandlerParam()
        setattr(cmdParam, "description", "Ticket 1")
        cmdParamCount = 1

        self.assertEqual(self.todo.getOpenedTicketsCount(), 0)
        res = self.cmd.runCommand(self.todo, cmdParamCount, cmdParam)
        self.assertEqual(res, CommandError.kOk)
        self.assertEqual(self.todo.getOpenedTicketsCount(), 1)

        res = self.cmd.runCommand(self.todo, cmdParamCount, cmdParam)
        self.assertEqual(res, CommandError.kOk)
        self.assertEqual(self.todo.getOpenedTicketsCount(), 2)

        ticketList = self.todo.getOpenedTickets()
        self.assertEqual(ticketList.getTicketByIndex(0).getDescription(), "Ticket 1")
        self.assertEqual(ticketList.getTicketByIndex(1).getDescription(), "Ticket 1")

class TestPrintTicket(unittest.TestCase):
    def setUp(self):
        self.todo = TodoManager()
        self.cmd  = CommandPrintTicket()

        cmdOpenTicket = CommandOpenTicket()
        cmdParam = HandlerParam()
        setattr(cmdParam, "description", "Ticket 1")
        cmdParamCount = 1

        res = cmdOpenTicket.runCommand(self.todo, cmdParamCount, cmdParam)
        self.assertEqual(res, CommandError.kOk)

    def runTest(self):
        cmdParam = HandlerParam()
        cmdParamCount = 1
        setattr(cmdParam, "ticketId", 1)

        res = self.cmd.runCommand(self.todo, cmdParamCount, cmdParam)
        self.assertEqual(res, CommandError.kOk)

        setattr(cmdParam, "ticketId", 2)
        res = self.cmd.runCommand(self.todo, cmdParamCount, cmdParam)
        self.assertEqual(res, CommandError.kError)

class TestCloseTicket(unittest.TestCase):
    def setUp(self):
        self.todo = TodoManager()
        self.cmd  = CommandCloseTicket() 

        cmdOpenTicket = CommandOpenTicket()
        cmdParam = HandlerParam()
        setattr(cmdParam, "description", "Ticket 1")
        cmdParamCount = 1

        res = cmdOpenTicket.runCommand(self.todo, cmdParamCount, cmdParam)
        self.assertEqual(res, CommandError.kOk)

    def runTest(self):
        cmdParam = HandlerParam()
        cmdParamCount = 1
        setattr(cmdParam, "ticketId", 1)

        self.assertEqual(self.todo.getOpenedTicketsCount(), 1)
        res = self.cmd.runCommand(self.todo, cmdParamCount, cmdParam)
        self.assertEqual(res, CommandError.kOk)
        self.assertEqual(self.todo.getOpenedTicketsCount(), 0)

        res = self.cmd.runCommand(self.todo, cmdParamCount, cmdParam)
        self.assertEqual(res, CommandError.kError)

        setattr(cmdParam, "ticketId", 2)
        res = self.cmd.runCommand(self.todo, cmdParamCount, cmdParam)
        self.assertEqual(res, CommandError.kError)


class TestAddTagToTicket(unittest.TestCase):
    def setUp(self):
        self.todo = TodoManager()
        self.cmd  = CommandAddTagToTicket() 

        addTagCmd  = CommandAddTag()
        cmdParam = HandlerParam()
        cmdParamCount = 1

        setattr(cmdParam, "name", "Tag1")
        res = addTagCmd.runCommand(self.todo, cmdParamCount, cmdParam)
        self.assertEqual(res, CommandError.kOk)

        setattr(cmdParam, "name", "Tag2")
        res = addTagCmd.runCommand(self.todo, cmdParamCount, cmdParam)
        self.assertEqual(res, CommandError.kOk)

        self.assertEqual(self.todo.getTagCount(), 2)

        self.tag1 = self.todo.getTagByName("Tag1")
        self.assertNotEqual(self.tag1, None)
        self.tag2 = self.todo.getTagByName("Tag2")
        self.assertNotEqual(self.tag2, None)

        cmdOpenTicket = CommandOpenTicket()
        cmdParam = HandlerParam()
        setattr(cmdParam, "description", "Ticket 1")
        cmdParamCount = 1

        res = cmdOpenTicket.runCommand(self.todo, cmdParamCount, cmdParam)
        self.assertEqual(res, CommandError.kOk)

    def runTest(self):
        cmdParam = HandlerParam()
        cmdParamCount = 2
        setattr(cmdParam, "ticketId", 1)
        setattr(cmdParam, "tagName", "Tag1")

        res = self.cmd.runCommand(self.todo, cmdParamCount, cmdParam)
        self.assertEqual(res, CommandError.kOk)

        ticket = self.todo.getTicketById(1)
        self.assertNotEqual(ticket, None)
        self.assertTrue(ticket.hasTag(self.tag1))
        self.assertFalse(ticket.hasTag(self.tag2))

        res = self.cmd.runCommand(self.todo, cmdParamCount, cmdParam)
        self.assertEqual(res, CommandError.kError)

        ticket = self.todo.getTicketById(1)
        self.assertNotEqual(ticket, None)
        self.assertTrue(ticket.hasTag(self.tag1))
        self.assertFalse(ticket.hasTag(self.tag2))

        cmdParam = HandlerParam()
        cmdParamCount = 2
        setattr(cmdParam, "ticketId", 1)
        setattr(cmdParam, "tagName", "Tag2")
        res = self.cmd.runCommand(self.todo, cmdParamCount, cmdParam)
        self.assertEqual(res, CommandError.kOk)

        ticket = self.todo.getTicketById(1)
        self.assertNotEqual(ticket, None)
        self.assertTrue(ticket.hasTag(self.tag1))
        self.assertTrue(ticket.hasTag(self.tag2))

        cmdParam = HandlerParam()
        cmdParamCount = 2
        setattr(cmdParam, "ticketId", 1)
        setattr(cmdParam, "tagName", "Tag3")
        res = self.cmd.runCommand(self.todo, cmdParamCount, cmdParam)
        self.assertEqual(res, CommandError.kError)

        ticket = self.todo.getTicketById(1)
        self.assertNotEqual(ticket, None)
        self.assertTrue(ticket.hasTag(self.tag1))
        self.assertTrue(ticket.hasTag(self.tag2))

        cmdParam = HandlerParam()
        cmdParamCount = 2
        setattr(cmdParam, "ticketId", 2)
        setattr(cmdParam, "tagName", "Tag1")
        res = self.cmd.runCommand(self.todo, cmdParamCount, cmdParam)
        self.assertEqual(res, CommandError.kError)

        ticket = self.todo.getTicketById(1)
        self.assertNotEqual(ticket, None)
        self.assertTrue(ticket.hasTag(self.tag1))
        self.assertTrue(ticket.hasTag(self.tag2))

if __name__ == '__main__':
    unittest.main()
