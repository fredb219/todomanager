import unittest
from todomanager import *

class TestTagManagement(unittest.TestCase):
    def setUp(self):
        self.todo = TodoManager()

    def runTest(self):
        tagName = "TestTag"
        tagNameMany = "TestTag %d"

        res, createdTag = self.todo.addTag(None)
        self.assertEqual(res, ErrorCode.kWrongParam)
        self.assertEqual(createdTag, None)

        tag = Tag()
        res, createdTag = self.todo.addTag(tag)
        self.assertEqual(res, ErrorCode.kWrongParam)
        self.assertEqual(createdTag, None)

        self.assertEqual(tag.getId(), None)
        self.assertEqual(tag.getName(), None)

        tag.setName(tagName)
        self.assertEqual(tag.getName(), tagName)

        res, createdTag = self.todo.addTag(tag)
        self.assertEqual(res, ErrorCode.kOk)
        self.assertNotEqual(createdTag, None)
        self.assertEqual(self.todo.getTagCount(), 1)

        tag = self.todo.getTagByName(tagName)
        self.assertNotEqual(tag, None)
        self.assertNotEqual(tag.getId(), None)
        self.assertEqual(tag.getName(), tagName)

        currentId = tag.getId()
        tag = self.todo.getTagById(currentId)
        self.assertNotEqual(tag, None)
        self.assertEqual(tag.getId(), currentId)
        self.assertEqual(tag.getName(), tagName)

        (res, createdTag) = self.todo.addTag(tag)
        self.assertEqual(res, ErrorCode.kTagAlreadyExist)
        self.assertEqual(createdTag, None)
        self.assertEqual(self.todo.getTagCount(), 1)

        res = self.todo.removeTag(tag)
        self.assertEqual(res, ErrorCode.kOk)
        self.assertEqual(self.todo.getTagCount(), 0)

        res = self.todo.removeTag(tag)
        self.assertEqual(res, ErrorCode.kTagNotFound)

        for i in range(10):
            tag = Tag()
            tag.setName(tagNameMany % (i + 1))
            (res, createdTag) = self.todo.addTag(tag)
            self.assertEqual(res, ErrorCode.kOk)

        self.assertEqual(self.todo.getTagCount(), 10)

        for i in range(10):
            tmpTagName = tagNameMany % (i + 1)

            tag = self.todo.getTagByName(tmpTagName)
            self.assertNotEqual(tag, None)

            res = self.todo.removeTag(tag)
            self.assertEqual(res, ErrorCode.kOk)

        self.assertEqual(self.todo.getTagCount(), 0)

class TestTicketManagement(unittest.TestCase):
    def setUp(self):
        self.todo = TodoManager()

        for i in range(3):
            tag = Tag()
            tag.setName("Tag %d" % (i + 1))
            (res, createdTag) = self.todo.addTag(tag)
            self.assertEqual(res, ErrorCode.kOk)

        self.wrongTag = Tag()
        self.wrongTag.setName("Wrong tag")

    def runTest(self):
        ticketDescription = "Amazing description...."

        (res, createdTicket) = self.todo.addTicket(None)
        self.assertEqual(res, ErrorCode.kWrongParam)
        self.assertEqual(createdTicket, None)

        tag1 = self.todo.getTagByName("Tag 1")
        self.assertNotEqual(tag1.getId(), None)

        tag2 = self.todo.getTagByName("Tag 2")
        self.assertNotEqual(tag2.getId(), None)

        tag3 = self.todo.getTagByName("Tag 3")
        self.assertNotEqual(tag3.getId(), None)

        ticket = Ticket()
        (res, createdTicket) = self.todo.addTicket(None)
        self.assertEqual(res, ErrorCode.kWrongParam)
        self.assertEqual(createdTicket, None)

        self.assertEqual(ticket.getId(), None)

        ticket.setStatus(TicketStatus.kOpened)
        ticket.setPriority(TicketPriority.kNormal)
        ticket.setDescription(ticketDescription)
        res = ticket.addTag(tag1)
        self.assertEqual(res, ErrorCode.kOk)
        res = ticket.addTag(tag2)
        self.assertEqual(res, ErrorCode.kOk)

        self.assertEqual(ticket.getStatus(), TicketStatus.kOpened)
        self.assertEqual(ticket.getPriority(), TicketPriority.kNormal)
        self.assertEqual(ticket.getDescription(), ticketDescription)
        self.assertTrue(ticket.hasTag(tag1))
        self.assertTrue(ticket.hasTag(tag2))
        self.assertFalse(ticket.hasTag(tag3))

        res = ticket.addTag(self.wrongTag)
        self.assertEqual(res, ErrorCode.kWrongParam)

        self.assertEqual(self.todo.getTicketCount(), 0)
        self.assertEqual(self.todo.getOpenedTicketsCount(), 0)

        (res, createdTicket) = self.todo.addTicket(ticket)
        self.assertEqual(res, ErrorCode.kOk)
        self.assertNotEqual(createdTicket, None)
        self.assertEqual(self.todo.getTicketCount(), 1)
        self.assertEqual(self.todo.getOpenedTicketsCount(), 1)

        ticket.setPriority(TicketPriority.kHigh)

        (res, createdTicket) = self.todo.addTicket(ticket)
        self.assertEqual(res, ErrorCode.kOk)
        self.assertNotEqual(createdTicket, None)
        self.assertEqual(self.todo.getTicketCount(), 2)
        self.assertEqual(self.todo.getOpenedTicketsCount(), 2)

        res = self.todo.addTagToTicket(createdTicket, tag3)
        self.assertEqual(res, ErrorCode.kOk)

        res = self.todo.addTagToTicket(createdTicket, tag3)
        self.assertEqual(res, ErrorCode.kTicketAlreadyHasTag)        
        
        ticket = self.todo.getTicketById(createdTicket.getId())
        self.assertNotEqual(ticket, None)
        self.assertTrue(ticket.hasTag(tag1))
        self.assertTrue(ticket.hasTag(tag2))
        self.assertTrue(ticket.hasTag(tag3))

        openedTickets = self.todo.getOpenedTickets()
        self.assertEqual(openedTickets.getTicketCount(), 2)

        openedTicketsTag1 = self.todo.getOpenedTicketsByTag(tag1)
        self.assertEqual(openedTicketsTag1.getTicketCount(), 2)

        openedTicketsTag3 = self.todo.getOpenedTicketsByTag(tag3)
        self.assertEqual(openedTicketsTag3.getTicketCount(), 1)

        openedTicketsPrioNormal = self.todo.getOpenedTicketsByPriority(TicketPriority.kNormal)
        self.assertEqual(openedTicketsPrioNormal.getTicketCount(), 1)

        openedTicketsPrioHigh = self.todo.getOpenedTicketsByPriority(TicketPriority.kHigh)
        self.assertEqual(openedTicketsPrioHigh.getTicketCount(), 1)

        res = self.todo.closeTicket(openedTickets.getTicketByIndex(0))
        self.assertEqual(res, ErrorCode.kOk)
        self.assertEqual(self.todo.getTicketCount(), 2)
        self.assertEqual(self.todo.getOpenedTicketsCount(), 1)

        openedTickets = self.todo.getOpenedTickets()
        self.assertEqual(openedTickets.getTicketCount(), 1)
        res = self.todo.removeTicket(openedTickets.getTicketByIndex(0))
        self.assertEqual(res, ErrorCode.kOk)
        self.assertEqual(self.todo.getTicketCount(), 1)
        self.assertEqual(self.todo.getOpenedTicketsCount(), 0)

if __name__ == '__main__':
    unittest.main()

