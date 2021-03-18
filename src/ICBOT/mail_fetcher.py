from contextlib import contextmanager
from re import S, U

from html2text import html2text
from imbox import Imbox
from imbox.messages import Messages

from ICBOT.constants import Constants

from .utils.logging import logger
from .var_env import PASSWORD_MAIL, USER_MAIL


class MailFetcher: 
    """Get latest mails from the channel.
    """

    def __init__(self) -> None:
        self.connect() 
    
    def connect(self):
        """Connects the imbox.
        """
        IMAP_SERVER = "imap.gmail.com"
        PORT = 993
        USER_MAIL = "icbotendpoint@gmail.com"
        PASSWORD_MAIL = "@a_4e6$9gSg:7EYN"
        try:
            self.imbox = Imbox(IMAP_SERVER, username=USER_MAIL, password=PASSWORD_MAIL, ssl=True)
        except Exception as e: 
            print(USER_MAIL, PASSWORD_MAIL)
            logger.critical("Mail service couldn't be initialized.")
            logger.critical(e)
            self.imbox = None
        else: 
            logger.info("Mail services has been correctly initiliazed.")
    
    def _fetch_last_emails(self) -> dict: 
        self.imbox.connection.NOOP()
        if (self.imbox is None): 
            logger.critical("Mails couldn't be fetched, because imbox is none")
            return
        resp = {}
        for section in Constants.SECTIONS:
            messages = self.imbox.messages(unread=True, label=section)
            if len(messages) > 0 : 
                uid, last_message = messages[-1] 
                logger.info(f"Mail has been fetched for {section}")
            else: 
                logger.info(f"Last mail is none for {section}")
                uid,last_message = None, None
            resp[section] = (uid, last_message)
            
        return resp
        
    def _parse_email(self, last_message: Messages) -> dict: 
        return {
            "sender": f"{last_message.sent_from[0]['name']} ({last_message.sent_from[0]['email']})",
            "object": last_message.subject, 
            "content": last_message.body["plain"][0], 
        }
        
    def _mark_read(self, uid) -> None:
        self.imbox.mark_seen(uid)
        
    @contextmanager
    def fetched_email(self) -> dict: 
        """Handle the last message fetching, and run logic if no exception has been raised.

        Yields
        -------
        dict 
            The dict where keys are the two sections, and as value a dict describing the mail (sender, object, content) (None if there aren't any).
        """
        mails_sections = self._fetch_last_emails()
        uids = []
        for section in mails_sections: 
            uid, message =  mails_sections[section]
            if uid is not None: 
                uids.append(uid)
                mails_sections[section] = self._parse_email(message)
            else :
                mails_sections[section] = None
        yield mails_sections
        for uid in uids: 
            self._mark_read(uid)
