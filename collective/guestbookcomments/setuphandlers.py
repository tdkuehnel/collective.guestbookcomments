import logging
PROFILE_ID='profile-collective.guestbookcomments:default'
from collective.guestbookcomments.interfaces import IGuestbookCommentLayer
from zope.component import queryUtility
from plone.browserlayer import utils as layerutils
from plone.browserlayer.interfaces import ILocalBrowserLayerType

def setupVarious(context, logger=None):

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('collective.guestbookcomments_various.txt') is None:
        return

    # Add additional setup code here
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('collective.guestbookcomments')        

    logger.info("ran setupVarious for collective.guestbookcomments")

def removeContent(context, logger=None):
    if context.readDataFile('collective.guestbookcomments_uninstall.txt') is None:
        return

    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('collective.guestbookcomments')        
        
#    portal = context.getSite()  
#    existing = queryUtility(ILocalBrowserLayerType, name='CollectiveGuestbookcomments', context=portal)
#    if existing:
#        sm = portal.getSiteManager()
#        success = sm.unregisterUtility(component=existing, provided=ILocalBrowserLayerType, name="CollectiveGuestbookcomments")
#        logger.info('unregister Browser layer "collective.guestbookcomments": '+ repr(success))
#    else:
#        logger.info('No Browser layer "collective.guestbookcomments" registered for '+ repr(portal))

    logger.info("ran uninstall for collective.guestbookcomments")
