from auth import get_gmail_service
import shared
from keywords import TRASH_KEYWORDS
from interface_langs import interface_langs 

import base64
import requests
import re
import time

# Get an authorized Gmail API client
service = get_gmail_service()

# Retrieve the List-Unsubscribe header
def list_unsubscribe_links(msg):
    for header in msg['payload']['headers']:
        if header['name'].lower() == 'list-unsubscribe':
            return header['value']
    return None

# Retrieving the sender's email
def get_sender(msg):
    for header in msg['payload']['headers']:
        if header['name'].lower() == 'from':
            return header['value']
    return 'Unknown sender'

# Parsing links and emails from the unsubscribe header
def parse_unsubscribe(unsubscribe_header):
    urls = re.findall(r'<(http[^>]*)>', unsubscribe_header)
    raw_emails = re.findall(r'<mailto:([^>]+)>', unsubscribe_header)

    emails = []
    for email in raw_emails:
        email = email.strip()
        if '?' in email:
            email = email.split('?')[0]
        if '@' in email:
            emails.append(email)

    return urls, emails


def send_unsubscribe_email(to_email):
    if '@' not in to_email:
        return
    message = f"To: {to_email}\r\nSubject: Unsubscribe\r\n\r\nUnsubscribe me."
    encoded_msg = base64.urlsafe_b64encode(message.encode('utf-8')).decode('utf-8')
    service.users().messages().send(
        userId='me',
        body={'raw': encoded_msg}
    ).execute()

def click_unsubscribe_link(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        requests.get(url, headers=headers, timeout=10)
    except:
        pass

def is_probably_spam(msg_data):
    subject = next(
        (h['value'] for h in msg_data['payload']['headers'] if h['name'].lower() == 'subject'),
        ''
    ).lower()
    for keyword in TRASH_KEYWORDS:
        if keyword in subject:
            return True

    parts = msg_data['payload'].get('parts', [])
    for part in parts:
        if part['mimeType'] == 'text/html':
            body_data = part['body'].get('data')
            if not body_data:
                continue
            html = base64.urlsafe_b64decode(body_data).decode('utf-8', errors='ignore').lower()
            for word in TRASH_KEYWORDS:
                if word in html:
                    return True

    return False

def find_unsubscribe_in_body(msg):
    parts = msg['payload'].get('parts', [])
    for part in parts:
        if part['mimeType'] == 'text/html':
            body_data = part['body'].get('data')
            if not body_data:
                continue
            html = base64.urlsafe_b64decode(body_data).decode('utf-8', errors='ignore').lower()

            keywords = [
                'unsubscribe', 'zrušit odběr', 'pokud si nepřejete',
                'click here to unsubscribe', 'unsubscribe here', 'odhlásit se', 'nepřejete si',
            ]

            for keyword in keywords:
                if keyword in html:
                    match = re.search(rf'{keyword}.*?href=[\'"]([^\'"]+)[\'"]', html)
                    if match:
                        return match.group(1)

                    href_match = re.search(r'href=[\'"]([^\'"]+)[\'"]', html)
                    if href_match:
                        return href_match.group(1)
    return None


def get_messages(limit=100, log_output=None, lang_code="en"):
    lang = interface_langs.get(lang_code, interface_langs['en'])
    log = print if log_output is None else lambda msg: log_output.insert('end', msg + '\n')
    log(lang["processing"].format(limit=limit))

    processed = 0
    next_page_token = None

    while processed < limit:
        max_results = min(100, limit - processed)
        response = service.users().messages().list(
            userId='me', labelIds=['INBOX'],
            maxResults=max_results, pageToken=next_page_token
        ).execute()

        messages = response.get('messages', [])
        if not messages:
            log(lang["no_more_messages"])
            break

        for msg in messages:
            if shared.stop_flag:
                log(lang["cancelled"])
                return
            if processed >= limit:
                break

            try:
                msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()

                label_ids = msg_data.get('labelIds', [])
                is_promotional = any(label in label_ids for label in [
                    'CATEGORY_PROMOTIONS', 'CATEGORY_SOCIAL', 'CATEGORY_UPDATES']
                )
                is_read = 'UNREAD' not in label_ids

                subject = next((h['value'] for h in msg_data['payload']['headers'] if h['name'] == 'Subject'), '')
                sender = get_sender(msg_data)

                if is_promotional and is_read:
                    log(lang["probably_spam"].format(subject=subject, sender=sender))
                    service.users().messages().trash(userId='me', id=msg['id']).execute()
                    processed += 1
                    continue

                unsubscribe = list_unsubscribe_links(msg_data)

                if unsubscribe:
                    log(lang["email_processing"])
                    log(lang["from"] + f" {sender}")
                    log(lang["unsubscribe_header_found"])

                    urls, emails = parse_unsubscribe(unsubscribe)

                    if urls:
                        click_unsubscribe_link(urls[0])
                        time.sleep(2)
                        service.users().messages().trash(userId='me', id=msg['id']).execute()
                        log(lang["deleted"])
                    elif emails:
                        send_unsubscribe_email(emails[0])
                        time.sleep(1)
                        service.users().messages().trash(userId='me', id=msg['id']).execute()
                        log(lang["deleted"])
                    else:
                        log(lang["no_link_found"])
                else:
                    url_from_body = find_unsubscribe_in_body(msg_data)
                    if url_from_body:
                        log(lang["found_in_body"] + f": {url_from_body}")
                        click_unsubscribe_link(url_from_body)
                        time.sleep(2)
                        try:
                            service.users().messages().trash(userId='me', id=msg['id']).execute()
                            log(lang["deleted"])
                        except Exception as e:
                            log(lang["delete_error"] + f" {e}")
                    else:
                        if is_probably_spam(msg_data):
                            log(lang["probably_spam"].format(subject=subject, sender=sender))
                            service.users().messages().trash(userId='me', id=msg['id']).execute()
                        else:
                            log(lang["skipped"])

                processed += 1

            except Exception as e:
                log(lang["process_error"] + f" {e}")
                continue

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break
