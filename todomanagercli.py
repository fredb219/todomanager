from todomanager import *
from shell import *
import shlex
import sys

FILEPATH = "todolist.bin"

def tagListToString(tagList):
    if len(tagList) == 0:
        return "No tag"

    firstItem = True
    strTagList = ""
    for tag in tagList:
        if firstItem == True:
            strTagList = tag.getName()
            firstItem = False
        else:
            strTagList = strTagList + ", %s" % tag.getName()

    return strTagList

class TodoManagerCommand(Command):
    def __init__(self, name, param_list = []):
        Command.__init__(self, name, param_list)

    def run(self, todo, paramCount, args):
        self.runCommand(todo, paramCount, args)
        TodoManager.saveToFile(todo, FILEPATH)

class CommandPrintTagList(TodoManagerCommand):
    def __init__(self):
        cmdName = "printTagList"
        Command.__init__(self, name=cmdName)

    def runCommand(self, todo, paramCount, args):
        print "Tag count : %d" % (todo.getTagCount())  
        for tag in todo.getTagList():
            print "Id %d : '%s'" % (tag.getId(), tag.getName())  

class CommandAddTag(TodoManagerCommand):
    def __init__(self):
        cmdName = "addTag"
        argList = [
            Parameter("name", ParameterType.STRING),
        ]

        Command.__init__(self, name=cmdName, param_list=argList)

    def runCommand(self, todo, paramCount, args):
        tag = Tag()
        tag.setName(args.name)

        (res, createdTag) = todo.addTag(tag)
        if res == ErrorCode.kOk:
            print "Tag '%s' created with Id %d" % (createdTag.getName(), createdTag.getId())
        else:
            print ErrorCode.toString(res)

class CommandPrintOpenedTicketList(TodoManagerCommand):
    def __init__(self):
        cmdName = "printOpenedTicketList"
        Command.__init__(self, name=cmdName)

    def runCommand(self, todo, paramCount, args):
        ticketList = todo.getOpenedTickets()
        print "Opened tickets count : %d" % (ticketList.getTicketCount())
        for ticket in ticketList.getContent():
            print "Id %d - '%s' - Tags : %s" % (ticket.getId(), ticket.getDescription(), tagListToString(ticket.getTagList()))

class CommandOpenTicket(TodoManagerCommand):
    def __init__(self):
        cmdName = "openTicket"
        argList = [
            Parameter("description", ParameterType.STRING),
        ]

        Command.__init__(self, name=cmdName, param_list=argList)

    def runCommand(self, todo, paramCount, args):
        ticket = Ticket()
        ticket.setDescription(args.description)
        ticket.setStatus(TicketStatus.kOpened)
        ticket.setPriority(TicketPriority.kNormal)

        (res, createdTicket) = todo.addTicket(ticket)
        if res == ErrorCode.kOk:
            print "Ticket '%s' created with Id %d" % (createdTicket.getDescription(), createdTicket.getId())
        else:
            print ErrorCode.toString(res)

class CommandPrintTicket(TodoManagerCommand):
    def __init__(self):
        cmdName = "printTicket"
        argList = [
            Parameter("ticketId", ParameterType.INTEGER),
        ]

        Command.__init__(self, name=cmdName, param_list=argList)

    def runCommand(self, todo, paramCount, args):
        ticket = todo.getTicketById(args.ticketId)
        if ticket != None:
            print "Ticket %d" % (ticket.getId())
            print "Status : %s" % (TicketStatus.toString(ticket.getStatus()))
            print "Priority : %s" % (TicketPriority.toString(ticket.getPriority()))
            print "Tag : %s" % tagListToString(ticket.getTagList())
            print "Description : %s" % (ticket.getDescription())
        else:
            print "Ticket %d not found" % (args.ticketId)

class CommandCloseTicket(TodoManagerCommand):
    def __init__(self):
        cmdName = "closeTicket"
        argList = [
            Parameter("ticketId", ParameterType.INTEGER),
        ]

        Command.__init__(self, name=cmdName, param_list=argList)

    def runCommand(self, todo, paramCount, args):
        ticket = todo.getTicketById(args.ticketId)
        if ticket != None:
            res = todo.closeTicket(ticket)
            if res == ErrorCode.kOk:
                print "Ticket %d closed" % (ticket.getId())
            else:
                print ErrorCode.toString(res)
        else:
            print "Ticket %d not found" % (args.ticketId)

class CommandAddTagToTicket(TodoManagerCommand):
    kTicketId = 0
    kTagName  = 1

    def __init__(self):
        cmdName = "addTagToTicket"
        argList = [
            Parameter("ticketId", ParameterType.INTEGER),
            Parameter("tagName",  ParameterType.STRING),
        ]

        Command.__init__(self, name=cmdName, param_list=argList)

    def runCommand(self, todo, paramCount, args):
        tag = todo.getTagByName(args.tagName)
        if tag == None:
            print "Tag %s does not exist" % (args.tagName)
            return

        ticket = todo.getTicketById(args.ticketId)
        if ticket == None:
            print "Ticket %d not found" % (args.ticketId)
            return

        res = todo.addTagToTicket(ticket, tag)
        if res != ErrorCode.kOk:
            print ErrorCode.toString(res)

    def completeParameter(self, todo, parameterIndex, parameterContent):
#        print "Param %d - '%s'" % (parameterIndex, parameterContent)

        if parameterIndex == CommandAddTagToTicket.kTagName:
            return [tag.getName() for tag in todo.getTagList() if tag.getName().startswith(parameterContent)] + [None]
        else:
            return [None]

if __name__ == '__main__':
    (res, todo) = TodoManager.loadFromFile(FILEPATH)
    if res != ErrorCode.kOk:
        print "Starting from empty content"

    sh = Shell(todo)    

    cmdList = [
        CommandPrintTagList(),
        CommandAddTag(),
        CommandPrintOpenedTicketList(),
        CommandOpenTicket(),
        CommandPrintTicket(),
        CommandCloseTicket(),
        CommandAddTagToTicket(),
    ]

    sh.register_command_list(cmdList)
    sh.cmdloop()

