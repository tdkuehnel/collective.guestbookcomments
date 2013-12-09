from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from collective.guestbookcomments import guestbookcommentsMessageFactory as _


class IGuestbookCommentAdded(Interface):
    """
    GuestbookCommentAdded view interface
    """

    def test():
        """ test method"""


class GuestbookCommentAdded(BrowserView):
    """
    GuestbookCommentAdded browser view
    """
    implements(IGuestbookCommentAdded)

#    index = ViewPageTemplateFile("templates/comment_added.pt")

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def test(self):
        """
        test method
        """
        dummy = _(u'a dummy string')

        return {'dummy': dummy}

    def __call__(self):
        return self.index()

