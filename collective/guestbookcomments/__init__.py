# -*- extra stuff goes here -*-
from zope.i18nmessageid import MessageFactory

guestbookcommentsMessageFactory = MessageFactory('collective.guestbookcomments')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
