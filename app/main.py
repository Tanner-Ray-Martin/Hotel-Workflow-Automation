from core.mail.outlook import Outlook


def get_outlook_messages():
    max_messages = 10
    outlook = Outlook()
    for message in outlook.scan_inbox():
        print(message.subject)
        if message.message_idx >= max_messages:
            break


if __name__ == "__main__":
    get_outlook_messages()
