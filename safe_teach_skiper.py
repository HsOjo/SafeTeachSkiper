import json

import requests


class SafeTeachSkiper:
    LOGIN_URL = 'http://weiban.mycourse.cn/pharos/login/login.do'
    LIST_SPECIAL_URL = 'http://weiban.mycourse.cn/pharos/project/listSpecial.do'
    LIST_COURSE_URL = 'http://weiban.mycourse.cn/pharos/usercourse/listCourse.do'
    FINISH_COURSE_URL = 'http://weiban.mycourse.cn/pharos/usercourse/finish.do'

    def __init__(self):
        self._session = requests.session()
        self._user = None  # type: dict
        self._info = None  # type: dict

    def _get_data(self, json_str, into_list=True):
        data = json.loads(json_str)  # type: dict
        result = data.get('data')
        if into_list and isinstance(result, list) and len(result) == 1:
            result = result[0]

        return result

    def login(self, tenant_code, key_number, password):
        form = {
            'tenantCode': tenant_code,
            'keyNumber': key_number,
            'password': password
        }
        resp = self._session.post(self.LOGIN_URL, form)
        resp_str = resp.content.decode()
        result = self._get_data(resp_str)
        self._user = result
        return result is not None

    def get_info(self):
        form = {
            'userId': self._user['userId'],
            'tenantCode': self._user['tenantCode'],
        }
        resp = self._session.post(self.LIST_SPECIAL_URL, form)
        resp_str = resp.content.decode()
        result = self._get_data(resp_str)
        self._info = result
        return result

    def list_course(self):
        form = {
            'userProjectId': self._info['id'],
            'chooseType': 3,
            'tenantCode': self._user['tenantCode'],
        }
        resp = self._session.post(self.LIST_COURSE_URL, form)
        resp_str = resp.content.decode()
        result = self._get_data(resp_str, False)
        return result

    def finish(self, course_id):
        form = {
            'userCourseId': course_id,
            'tenantCode': self._user['tenantCode'],
        }
        resp = self._session.get(self.FINISH_COURSE_URL, params=form)
        resp_str = resp.content.decode()
        return 'ok' in resp_str
