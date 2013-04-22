#!/usr/bin/python
import calendar
import datetime
import json
import optparse
import paramiko
from pprint import pprint
import sys


optparser = optparse.OptionParser()
optparser.add_option('-p', '--project', default='swift',
                     help='Project to generate stats for')
optparser.add_option('-d', '--days', type='int', default=14,
                     help='Number of days to consider')
optparser.add_option('-r', '--raw', action='store_true', default=False,
                     help='Um... Hard to explain. Try it and see')

options, args = optparser.parse_args()

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.load_system_host_keys()
changes = []
while True:
    client.connect('review.openstack.org', port=29418,
                   key_filename='/Users/john/.ssh/id_rsa_launchpad',
                   username='notmyname')
    cmd = ('gerrit query project:openstack/%s '
           '--all-approvals --patch-sets --format JSON' % options.project)
    if len(changes) > 0:
        cmd += ' resume_sortkey:%s' % changes[-2]['sortKey']
    stdin, stdout, stderr = client.exec_command(cmd)
    for l in stdout:
        changes += [json.loads(l)]
    if changes[-1]['rowCount'] == 0:
        break

reviews = []

for change in changes:
    #print json.dumps(change, sort_keys=True, indent=4)
    for patchset in change.get('patchSets', []):
        for review in patchset.get('approvals', []):
            reviews += [review]

if not options.raw:
    cut_off = datetime.datetime.now() - datetime.timedelta(days=options.days)
    ts = calendar.timegm(cut_off.timetuple())
    reviews = filter(lambda x:x['grantedOn'] > ts, reviews)

def round_to_day(ts):
    SECONDS_PER_DAY = 60*60*24
    return (ts / (SECONDS_PER_DAY)) * SECONDS_PER_DAY

reviewers = {}
for review in reviews:
    if review['type'] != 'CRVW':
        # Only count code reviews.  Don't add another for Approved, which is
        # type 'APRV'
        continue
    reviewer = review['by'].get('username', 'unknown')
    reviewers.setdefault(reviewer,
            {'votes': {'-2': 0, '-1': 0, '1': 0, '2': 0}})
    reviewers[reviewer]['total'] = reviewers[reviewer].get('total', 0) + 1
    cur = reviewers[reviewer]['votes'][review['value']]
    reviewers[reviewer]['votes'][review['value']] = cur + 1

print json.dumps(reviewers, sort_keys=True, indent=4)
