import oss2

from app.config.secure import ALIYUN_OSS_BUCKET_NAME, ALIYUN_ACCESS_KEY_ID, ALIYUN_ACCESS_KEY_SECRET, FILE_URL

auth = oss2.Auth(ALIYUN_ACCESS_KEY_ID, ALIYUN_ACCESS_KEY_SECRET)
bucket = oss2.Bucket(auth, 'http://oss-cn-hangzhou.aliyuncs.com', ALIYUN_OSS_BUCKET_NAME)


def upload_to_oss(filename, data):
    bucket.put_object(filename, data)
    url = FILE_URL + filename
    return url
