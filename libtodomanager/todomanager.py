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

__all__ = [
    "ErrorCode",
    "TicketStatus",
    "TicketPriority",
    "Tag",
    "Ticket",
    "TicketList",
    "TodoManager"
]

class ErrorCode:
    kOk  = 1
    kErr = 2
    kTagAlreadyExist = 3
    kTagNotFound = 4
    kTicketNotFound = 5
    kFailToOpenFile = 6
    kWrongParam = 7
    kTicketAlreadyClosed = 8
    kTicketClosed = 9
    kTicketAlreadyHasTag = 10

    @staticmethod
    def toString(errCode):
        errorCodeStr = {
            ErrorCode.kOk: "Ok",
            ErrorCode.kErr: "Unknown error",
            ErrorCode.kTagAlreadyExist: "The tag already exists",
            ErrorCode.kTagNotFound: "Tag not found",
            ErrorCode.kTicketNotFound: "Ticket not found",
            ErrorCode.kFailToOpenFile: "Unable to open file",
            ErrorCode.kWrongParam: "Wrong param",
            ErrorCode.kTicketAlreadyClosed: "Ticket already closed",
            ErrorCode.kTicketClosed: "Ticket closed",
            ErrorCode.kTicketAlreadyHasTag: "Ticket already has this tag",
        }

        return errorCodeStr[errCode]

class TicketStatus:
    kOpened  = 1
    kClosed  = 2
    kDelayed = 3

    @staticmethod
    def toString(status):
        ticketStatusStr = {
            TicketStatus.kOpened:  "Opened",
            TicketStatus.kClosed:  "Closed",
            TicketStatus.kDelayed: "Delayed"
        }

        return ticketStatusStr[status]

class TicketPriority:
    kHigh   = 1
    kNormal = 2
    kLow    = 3

    @staticmethod
    def toString(priority):
        ticketPriorityStr = {
            TicketPriority.kHigh:   "High",
            TicketPriority.kNormal: "Normal",
            TicketPriority.kLow:    "Low"
        }

        return ticketPriorityStr[priority]

class Tag:
    def __init__(self):
        self.id   = None
        self.name = None

    def clone(self):
        ret = Tag()

        ret.id   = self.id
        ret.name = self.name

        return ret

    @staticmethod
    def isValid(tag, checkId = False):
        if checkId == False:
            return (tag.name != None)
        else:
            return (tag.name != None and tag.id != None)

    def setId(self, id):
        self.id = id

    def getId(self):
        return self.id

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def toString(self):
        return "Tag - Id %d - Name %s" % (self.id, self.name)

class Ticket:
    def __init__(self):
        self.id          = None
        self.tagList     = []
        self.description = None
        self.priority    = None
        self.status      = None

    def clone(self):
        ret = Ticket()

        ret.id          = self.id

        ret.tagList     = []
        for tag in self.tagList:
            ret.tagList.append(tag.clone())

        ret.description = self.description
        ret.priority    = self.priority
        ret.status      = self.status

        return ret

    @staticmethod
    def isValid(ticket):
        return (ticket.description != None and ticket.priority != None and ticket.status != None)

    def setId(self, id):
        self.id = id

    def getId(self):
        return self.id

    def setStatus(self, status):
        self.status = status

    def getStatus(self):
        return self.status

    def addTag(self, tag):
        if tag == None:
            return ErrorCode.kWrongParam
        elif False == Tag.isValid(tag, checkId=True):
            return ErrorCode.kWrongParam
        else:
            self.tagList.append(tag)
            return ErrorCode.kOk

    def getTagList(self):
        return self.tagList

    def hasTag(self, iTag):
        for tag in self.tagList:
            if tag.id == iTag.id:
                return True

        return False

    def setDescription(self, description):
        self.description = description

    def getDescription(self):
        return self.description

    def setPriority(self, priority):
        self.priority = priority

    def getPriority(self):
        return self.priority

    def toString(self):
        return "Ticket - Id %d - Tag %s - Priority %s - Status %s - Description %s" % (self.id, self.tag.getId(), ticketPriorityStr[self.priority], ticketStatusStr[self.status], self.description)

class TicketList:
    def __init__(self):
        self.ticketList = []

    def addTicket(self, ticket):
        self.ticketList.append(ticket)

    def getTicketCount(self):
        return len(self.ticketList)

    def getTicketByIndex(self, index):
        if index < 0:
            return None
        elif index > len(self.ticketList):
            return None
        else:
            return self.ticketList[index]

    def getContent(self):
        return self.ticketList

class TodoManager:
    def __init__(self, serializer=None):
        self.tagList   = []
        self.ticketList    = []
        self.tagLastId = 0
        self.ticketLastId  = 0
        self.serializer = serializer

    def setSerializer(self, serializer):
        self.serializer = serializer

    def save(self):
        self.serializer.save(self)

    def addTag(self, tag):
        if tag == None:
            return (ErrorCode.kWrongParam, None)
        elif False == Tag.isValid(tag):
            return (ErrorCode.kWrongParam, None)

        existingTag = self.getTagByName(tag.getName())
        if existingTag != None:
            return (ErrorCode.kTagAlreadyExist, None)

        self.tagLastId = self.tagLastId + 1
        tag.setId(self.tagLastId)
        self.tagList.append(tag)

        return (ErrorCode.kOk, tag.clone())

    def removeTag(self, tag):
        if tag == None:
            return ErrorCode.kWrongParam

        existingTag = self.getTagByIdInternal(tag.getId())
        if existingTag == None:
            return ErrorCode.kTagNotFound

        self.tagList.remove(existingTag)
        return ErrorCode.kOk

    def getTagList(self):
        ret = []

        for tag in self.tagList:
            ret.append(tag.clone())

        return ret

    def getTagCount(self):
        return len(self.tagList)

    def getTagByName(self, tagName):
        retval = None
        for tag in self.tagList:
            if tag.name == tagName:
                retval = tag.clone()
                break

        return retval

    def getTagByIdInternal(self, tagId):
        if tagId == None:
            return None

        retval = None
        for tag in self.tagList:
            if tag.id == tagId:
                retval = tag
                break

        return retval

    def getTagById(self, tagId):
        tag = self.getTagByIdInternal(tagId)
        if tag != None:
            return tag.clone()
        else:
            return None

    def addTicket(self, ticket):
        if ticket == None:
            return (ErrorCode.kWrongParam, None)
        elif False == Ticket.isValid(ticket):
            return (ErrorCode.kWrongParam, None)

        self.ticketLastId = self.ticketLastId + 1

        internalTicket = ticket.clone()
        internalTicket.setId(self.ticketLastId)
        self.ticketList.append(internalTicket)

        return (ErrorCode.kOk, internalTicket.clone())

    def addTagToTicket(self, ticket, tag):
        if ticket == None:
            return ErrorCode.kWrongParam
        elif Ticket.isValid(ticket) == False:
            return ErrorCode.kWrongParam
        elif tag == None:
            return ErrorCode.kWrongParam
        elif Tag.isValid(tag, checkId=True) == False:
            return ErrorCode.kWrongParam

        existingTag = self.getTagByIdInternal(tag.getId())
        if existingTag == None:
            return ErrorCode.kTagNotFound

        existingTicket = self.getTicketByIdInternal(ticket.getId())
        if existingTicket == None:
            return ErrorCode.kTicketNotFound
        elif existingTicket.getStatus() == TicketStatus.kClosed:
            return ErrorCode.kTicketClosed

        if existingTicket.hasTag(existingTag):
            return ErrorCode.kTicketAlreadyHasTag

        existingTicket.addTag(existingTag)

        return ErrorCode.kOk

    def closeTicket(self, ticket):
        existingTicket = self.getTicketByIdInternal(ticket.getId())
        if existingTicket == None:
            return ErrorCode.kTicketNotFound
        elif existingTicket.getStatus() == TicketStatus.kClosed:
            return ErrorCode.kTicketAlreadyClosed

        existingTicket.setStatus(TicketStatus.kClosed)

        return ErrorCode.kOk

    def removeTicket(self, ticket):
        existingTicket = self.getTicketByIdInternal(ticket.getId())
        if existingTicket == None:
            return ErrorCode.kTicketNotFound

        self.ticketList.remove(existingTicket)

        return ErrorCode.kOk

    def getTicketByIdInternal(self, ticketId):
        if ticketId == None:
            return None

        retval = None
        for ticket in self.ticketList:
            if ticket.id == ticketId:
                retval = ticket
                break

        return retval

    def getTicketById(self, ticketId):
        ticket = self.getTicketByIdInternal(ticketId)
        if ticket != None:
            return ticket.clone()
        else:
            return None

    def getTicketCount(self):
        return len(self.ticketList)

    def getOpenedTickets(self):
        retTicketList = TicketList()

        for ticket in self.ticketList:
            if TicketStatus.kOpened == ticket.getStatus():
                retTicketList.addTicket(ticket.clone())

        return retTicketList

    def getOpenedTicketsCount(self):
        return self.getOpenedTickets().getTicketCount()

    def getOpenedTicketsByTag(self, tag):
        retTicketList = TicketList()

        for ticket in self.ticketList:
            if ticket.hasTag(tag) and TicketStatus.kOpened == ticket.getStatus():
                retTicketList.addTicket(ticket.clone())

        return retTicketList

    def getOpenedTicketsByPriority(self, priority):
        retTicketList = TicketList()

        for ticket in self.ticketList:
            if ticket.getPriority() == priority and TicketStatus.kOpened == ticket.getStatus():
                retTicketList.addTicket(ticket.clone())

        return retTicketList

