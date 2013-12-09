from Products.Archetypes.public import BooleanField
from archetypes.schemaextender.field import ExtensionField

from zope.component import adapts
from zope.interface import implements
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender, IBrowserLayerAwareExtender
from Products.Archetypes.public import BooleanWidget
from Products.ATContentTypes.interface import IATDocument

from collective.guestbookcomments import guestbookcommentsMessageFactory as _
from collective.guestbookcomments.interfaces import IGuestbookCommentLayer

class CollectiveGuestbookEnabled(ExtensionField, BooleanField):
    """A Guestbook enabled/disabled field."""


class PageExtender(object):
    adapts(IATDocument)
    implements(IOrderableSchemaExtender, IBrowserLayerAwareExtender )
    
    layer = IGuestbookCommentLayer

    fields = [
        CollectiveGuestbookEnabled("guestbookDiscussion",
                                   schemata="settings",
                                   widget = BooleanWidget(
                                       label=_(u"Enable guestbook style comments"),
                                       description=_(u"Show the comments as guestbook entries with new entries on top"))),
    ]

    def getOrder(self, schematas):
        """ Manipulate the order in which fields appear.

        @param schematas: Dictonary of schemata name -> field lists

        @return: Dictionary of reordered field lists per schemata.
        """
        schematas["settings"] = ['allowDiscussion','guestbookDiscussion', 'excludeFromNav', 'presentation', 'tableContents']

        return schematas

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields
