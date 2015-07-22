__author__ = 'eugene'


import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

flags = None
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Quickstart'

def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'gmail-quickstart.json')
    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatability with Python 2.6
            credentials = tools.run(flow, store)
        print 'Storing credentials to ' + credential_path
    return credentials

def get_service():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    return service

# test
service = get_service()
# results = service.users().labels().list(userId='me').execute()
# labels = results.get('labels', [])
from pprint import pprint
# pprint(results)


def get_labels(k):
    msg = service.users().messages().get(userId='me', id=k).execute()
    return { 'key': k, 'labels': msg.get('labelIds')}

# check activity based on get unread messages and compare to read messages after timer / # based on writing too
def get_unread_keys():
    import itertools
    unread_keys = []
    keys = service.users().messages().list(userId='me', maxResults=10).execute()
    for k in itertools.islice(keys.get('messages'),0,10):
        msg = service.users().messages().get(userId='me', id=k.get('id')).execute()
        if('UNREAD' in msg.get('labelIds')):
            unread_keys.append(k.get('id'))
    # pprint(unread_keys)
    print 'unread keys %s: ' % unread_keys
    return unread_keys

#                            {u'name': u'Subject',
#                             u'value': u'12 things you may have missed on Sosh'},
def is_changed(unread_keys):
    for k in unread_keys:
        msg = service.users().messages().get(userId='me', id=k).execute()
        if('UNREAD' not in msg.get('labelIds')):
            print 'changed: %s' % msg.get('snippet')
            return True
    return False

unread_keys = get_unread_keys()
# is_c = is_changed(unread_keys)
# 'changes' if is_c else 'no changes'

def write_file(msg):
    # write in binary mode
    with open("gmail_status.csv", "ab") as f:
        #f.write('test\n')
        # m = str(time.time()) + ",1\r"
        print msg
        f.write(msg + '\n')
        f.close()
# write_file('test\n')
# write_file('test2\n')

# setup of logger
def create_logger():
    import logging
    import time
    from logging.handlers import RotatingFileHandler
    logger = logging.getLogger("Rotating Log")
    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler("gmail_status.csv", maxBytes=4000000, backupCount=5)
    logger.addHandler(handler)
    return logger

logger = create_logger()

def write_to_log(msg):
    print 'log: %s' % msg
    logger.info(msg)
# write_to_log('test')

# scheduling
# t = time.time()
# print time.localtime( t)
# print time.asctime( time.localtime(time.time()) )
SCHEDULE_INTERVAL = 30
import sched, time
s = sched.scheduler(time.time, time.sleep)
# def process_event(sc):
#     global unread_keys
#     msg = str(time.time()) + "," + ("1" if is_changed(unread_keys) else "0") # + '\n'
#     write_file(msg)
#     unread_keys = get_unread_keys()
#     sc.enter(SCHEDULE_INTERVAL, 1, process_event, (sc,))
def process_event(sc):
    global unread_keys
    prev_unread_keys = unread_keys
    unread_keys = get_unread_keys()
    msg = str(time.time()) + "," + ("1" if is_changed(prev_unread_keys) else "0") # + '\n'
    # write_file(msg)
    write_to_log(msg)
    sc.enter(SCHEDULE_INTERVAL, 1, process_event, (sc,))

# running
s.enter(SCHEDULE_INTERVAL, 1, process_event, (s,))
s.run()

# timestamp,activity,new_unread_items,checked_read_items,write_items
# 43243411232,1,


