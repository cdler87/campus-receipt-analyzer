def filter_receipts(emails):
    filtered = []

    for email in emails:
        sender = (email.get("sender") or "").lower()
        subject = (email.get("subject") or "").lower()

        if (
            "mobileorder@transactcampus.com" in sender
            or (
                "receipt" in subject
            )
        ):
            filtered.append(email)

    return filtered