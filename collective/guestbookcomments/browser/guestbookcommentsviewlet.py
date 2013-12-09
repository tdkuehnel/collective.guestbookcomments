from Acquisition import aq_inner
from plone.app.discussion.interfaces import IConversation
from plone.app.discussion.interfaces import IComment
from plone.app.discussion.interfaces import IDiscussionSettings
from plone.app.discussion.browser.comments import CommentsViewlet, CommentForm
from plone.registry.interfaces import IRegistry
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from z3c.form import form, field, button, interfaces
from z3c.form.interfaces import IFormLayer
from plone.z3cform.interfaces import IWrappedForm
from plone.z3cform import z2
from zope.i18n import translate
from zope.i18nmessageid import Message
from zope.component import createObject, queryUtility
from zope.interface import alsoProvides
from Products.Five.browser import BrowserView
from collective.guestbookcomments import guestbookcommentsMessageFactory as _
from guestbookcommentform import GuestbookCommentForm

import logging

COMMENT_DESCRIPTION_PLAIN_TEXT = _(
    u"comment_description_plain_text",
    default=u"You can add your guestbook entry by filling out the form below. " +
            u"Plain text formatting.")

COMMENT_DESCRIPTION_MARKDOWN = _(
    u"comment_description_markdown",
    default=u"You can add your guestbook entry by filling out the form below. " +
            u"Plain text formatting. You can use the Markdown syntax for " +
            u"links and images.")

COMMENT_DESCRIPTION_INTELLIGENT_TEXT = _(
    u"comment_description_intelligent_text",
    default=u"You can add your guestbook entry by filling out the form below. " +
            u"Plain text formatting. Web and email addresses are " +
            u"transformed into clickable links.")

COMMENT_DESCRIPTION_MODERATION_ENABLED = _(
    u"comment_description_moderation_enabled",
    default=u"Entries into the guestbook are moderated.")

class GuestbookCommentsViewlet(CommentsViewlet):

    guestbookform = GuestbookCommentForm
    guestbookindex = ViewPageTemplateFile('templates/guestbookcomments.pt')

    def update(self):
        super(CommentsViewlet, self).update()
        discussion_allowed = self.is_discussion_allowed()
        anonymous_allowed_or_can_reply = (
            self.is_anonymous()
            and self.anonymous_discussion_allowed()
            or self.can_reply()
        )
        if discussion_allowed and anonymous_allowed_or_can_reply:
            z2.switch_on(self, request_layer=IFormLayer)
            if self.is_guestbook():
                self.form = self.guestbookform(aq_inner(self.context), self.request)
            else:
                self.form = self.form(aq_inner(self.context), self.request)
            alsoProvides(self.form, IWrappedForm)
            self.form.update()

    def get_commenter_portrait(self, username=None):

        if username is None:
            # return the default user image if no username is given
#            return 'bluemlein.gif'
            return 'defaultUser.png'
        else:
            portal_membership = getToolByName(self.context,
                                              'portal_membership',
                                              None)
            user_portrait = portal_membership\
                .getPersonalPortrait(username)\
                .absolute_url()
            #return user_portrait.replace("defaultUser.png","bluemlein.gif")
            return user_portrait

    def is_guestbook(self):
        context = aq_inner(self.context)
        return context.guestbookDiscussion

    def get_replies(self, workflow_actions=False):
        """Returns all replies to a content object.
        
        If workflow_actions is false, only published
        comments are returned.

        If workflow actions is true, comments are
        returned with workflow actions.

        Order the comments guestbook-style
        """
        if not self.is_guestbook():
            return super(GuestbookCommentsViewlet, self).get_replies(workflow_actions)

        context = aq_inner(self.context)
        conversation = IConversation(context, None)

        if conversation is None:
            return iter([])

        wf = getToolByName(context, 'portal_workflow')

        # workflow_actions is only true when user
        # has 'Manage portal' permission

        def ordered_comments_list():
            # returns ordered comments list for guestbook display
            comments_list = []
            for root_comment in conversation.getThreads(depth=0):
                comments_list.insert(0, root_comment)
                reply_pos = 1
                for reply_comment in conversation.getThreads(root=root_comment["id"]):
                    reply_comment["depth"] += 1 # getThreads returns relative depth values !
                    comments_list.insert(reply_pos, reply_comment)
                    reply_pos += 1
            return comments_list

        def replies_with_workflow_actions():
            # Generator that returns replies dict with workflow actions
#            for r in conversation.getThreads():
            for r in ordered_comments_list():
                comment_obj = r['comment']
                # list all possible workflow actions
                actions = [
                    a for a in wf.listActionInfos(object=comment_obj)
                    if a['category'] == 'workflow' and a['allowed']
                ]
                r = r.copy()
                r['actions'] = actions
                yield r

        def published_replies():
            # Generator that returns replies dict with workflow status.
#            for r in conversation.getThreads():
            for r in ordered_comments_list():
                comment_obj = r['comment']
                workflow_status = wf.getInfoFor(comment_obj, 'review_state')
                if workflow_status == 'published':
                    r = r.copy()
                    r['workflow_status'] = workflow_status
                    yield r

        # Return all direct replies

        if len(conversation.objectIds()):
            if workflow_actions:
                return replies_with_workflow_actions()
            else:
                return published_replies()

    def comment_transform_message(self):
        """Returns the description that shows up above the comment text,
           dependent on the text_transform setting and the comment moderation
           workflow in the discussion control panel.
        """
        context = aq_inner(self.context)
        registry = queryUtility(IRegistry)
        settings = registry.forInterface(IDiscussionSettings, check=False)

        # text transform setting
        if settings.text_transform == "text/x-web-intelligent":
            message = translate(Message(COMMENT_DESCRIPTION_INTELLIGENT_TEXT),
                                context=self.request)
        elif settings.text_transform == "text/x-web-markdown":
            message = translate(Message(COMMENT_DESCRIPTION_MARKDOWN),
                                context=self.request)
        else:
            message = translate(Message(COMMENT_DESCRIPTION_PLAIN_TEXT),
                                context=self.request)

        # comment workflow
        wftool = getToolByName(context, "portal_workflow", None)
        workflow_chain = wftool.getChainForPortalType('Discussion Item')
        if workflow_chain:
            comment_workflow = workflow_chain[0]
            comment_workflow = wftool[comment_workflow]
            # check if the current workflow implements a pending state. If this
            # is true comments are moderated
            if 'pending' in comment_workflow.states:
                message = message + " " + \
                    translate(Message(COMMENT_DESCRIPTION_MODERATION_ENABLED),
                              context=self.request)

        return message

    def render(self):
        logger = logging.getLogger('collective.guestbookcomments')        
        if self.is_guestbook():
            logger.info("render for is_guestbook called")
            return self.guestbookindex()
        else:
            logger.info("render for not is_guestbook called")
            return super(GuestbookCommentsViewlet, self).render()
