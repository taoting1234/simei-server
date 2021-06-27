from flask import jsonify, request
from flask_login import login_required

from app.config.secure import ALLOWED_FILE_SUFFIX
from app.libs.error_code import ParameterException
from app.libs.helper import md5
from app.libs.red_print import RedPrint
from app.libs.service import upload_to_oss

api = RedPrint('file')


@api.route("", methods=['POST'])
@login_required
def create_file_api():
    file = request.files.get('file')
    if file is None:
        raise ParameterException('File is not exist')
    if len(file.filename.split('.')) == 1:
        raise ParameterException('File suffix is not exist')
    suffix = file.filename.split('.')[-1].lower()
    if suffix not in ALLOWED_FILE_SUFFIX:
        raise ParameterException('File suffix is not allowed')
    contents = file.read()
    filename = "{}.{}".format(md5(contents), suffix)
    res = upload_to_oss(filename, contents)
    return jsonify({
        'code': 0,
        'data': res
    })
