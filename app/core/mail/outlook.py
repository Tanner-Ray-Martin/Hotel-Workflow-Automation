import win32com.client

from resources.configs.email_settings import (
    INBOX_NAME,
    FROM_EMAIL,
    SORT_BY_DATE_RECEIVED,
    EMAIL_CONNECTION_TYPE,
)
from models.outlook_models import OutlookMessage


class Outlook:
    def __init__(self):
        if EMAIL_CONNECTION_TYPE == "MAPI":
            outlook = win32com.client.Dispatch("Outlook.Application")
            self.namespace = outlook.GetNamespace(EMAIL_CONNECTION_TYPE)
            self.inbox = self.get_mapi_inbox_folder(self.namespace)
            if not self.inbox:
                raise Exception(f"Could not find inbox folder: {INBOX_NAME}")

    def get_mapi_inbox_folder(
        self, current_folder: object, inbox_name: str = INBOX_NAME
    ) -> object:
        return_folder = None

        for folder in current_folder.Folders:  # type: ignore
            if folder.Name == inbox_name:
                return folder
            else:
                if not return_folder:
                    return_folder = self.get_mapi_inbox_folder(folder, inbox_name)

        return return_folder

    def is_wanted_email(self, message: object) -> bool:
        excchange_user = message.Sender.GetExchangeUser()  # type: ignore
        if excchange_user is None:
            return False
        sender = excchange_user.PrimarySmtpAddress  # type: ignore
        if sender is None:
            return False
        return sender == FROM_EMAIL  # type: ignore

    def scan_inbox(self):
        messages = self.inbox.Items  # type: ignore
        if SORT_BY_DATE_RECEIVED:
            messages.Sort("[ReceivedTime]", SORT_BY_DATE_RECEIVED)

        for message_idx, message in enumerate(messages):
            if self.is_wanted_email(message):
                yield OutlookMessage(
                    message_idx=message_idx,
                    subject=message.Subject,
                    html_body=message.HTMLBody,
                    sender=message.Sender.GetExchangeUser().PrimarySmtpAddress,
                    received_time=message.ReceivedTime,
                )


if __name__ == "__main__":
    outlook = Outlook()
    for message in outlook.scan_inbox():
        print(message)
