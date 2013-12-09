from zope.interface import implements, Interface
from plone.app.discussion.interfaces import IComment
from zope import schema
from collective.guestbookcomments import guestbookcommentsMessageFactory as _

class IGuestbookCommentLayer(Interface):
    """
    Guestbook comments Browserlayer interface
    """

class IGuestbookComment(IComment):
    """A guestbook style comment.

    subclassing is done only to have own set of translations for widget labels.
    """

    title = schema.TextLine(title=_(u"label_subject",
                                    default=u"Subject"))

    text = schema.Text(
        title=_(
            u"label_comment",
            default=u"Comment"
        )
    )

