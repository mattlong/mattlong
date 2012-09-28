import hashlib

import boto
from boto.s3.key import Key

filename = '/etc/mattlong.org/defaultdb'

with open('/etc/mattlong.org/backup_credentials', 'r') as fp:
    access_key, secret_key = fp.read().strip().split(',')

conn = boto.connect_s3(access_key, secret_key)
bucket = conn.get_bucket('mattlong-versioned')
key = bucket.get_key('mattlong_org/defaultdb')

last_backup_md5 = key.etag.strip('"')
current_md5 = hashlib.md5(open(filename, 'rb').read()).hexdigest()

if current_md5 != last_backup_md5:
    print 'uploading new version [%s]' % (current_md5,)
    key.set_contents_from_filename(filename)
