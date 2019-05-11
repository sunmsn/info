#!/usr/bin/python
# -*- coding: utf-8 -*-

import os,sys
import string
import oss2

access_key_id = '<你的AccessKeyId>'
access_key_secret = '<你的AccessKeySecret>'
bucket_name = '<你的Bucket>'
endpoint = '<你的Bucket访问域名>'

file_dir = '' if sys.argv[1] == '.' else sys.argv[1]+"/"
file_name = sys.argv[2]

bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)
total_size = os.path.getsize(file_name)
part_size = oss2.determine_part_size(total_size, preferred_size=128 * 1024)
key = file_dir+file_name
upload_id = bucket.init_multipart_upload(key).upload_id

if len(sys.argv) > 3:
    bucket.delete_object(key)
else:
    with open(file_name, 'rb') as fileobj:
        parts = []
        part_number = 1
        offset = 0
        while offset < total_size:
            num_to_upload = min(part_size, total_size - offset)
            result = bucket.upload_part(key, upload_id, part_number,oss2.SizedFileAdapter(fileobj, num_to_upload))
            parts.append(oss2.models.PartInfo(part_number, result.etag))
            offset += num_to_upload
            part_number += 1
        bucket.complete_multipart_upload(key, upload_id, parts)
