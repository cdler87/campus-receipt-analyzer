import os
import email
from email import policy

def load_eml_emails(folder_path):
    emails = []

    for i, filename in enumerate(os.listdir(folder_path)):
        if not filename.endswith(".eml"):
            continue

        file_path = os.path.join(folder_path, filename)

        with open(file_path, "rb") as f:
            msg = email.message_from_binary_file(f, policy=policy.default)

        subject = msg["subject"]
        sender = msg["from"]
        date = msg["date"]

        # Extract body
        if msg.is_multipart():
            parts = []
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    parts.append(part.get_content())
            body = "\n".join(parts)
        else:
            body = msg.get_content()

        emails.append({
            "message_id": filename,
            "subject": subject,
            "sender": sender,
            "timestamp": date,
            "body_text": body
        })

    return emails