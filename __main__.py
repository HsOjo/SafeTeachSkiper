from safe_teach_skiper import SafeTeachSkiper

print('''如学校为深圳职业技术学院，学校代码留空即可，否则请自行抓包。
详情请查看README，项目地址：https://github.com/HsOjo/SafeTeachSkiper
''')

tenant_code = input('学校代码:')
if tenant_code == '':
    tenant_code = '51800001'
key_number = input('学号:')
password = input('密码:')

client = SafeTeachSkiper()
print('登录成功' if client.login(tenant_code, key_number, password) else '登录失败')
print(client.get_info())

course_list = client.list_course()
for course in course_list:
    for item in course['courseList']:
        if item['finished'] == 2:
            try:
                result = client.finish(item['userCourseId'])
                print(item['resourceName'], '已完成' if result else '未完成')
            except:
                print(item['resourceName'], '出错')
        else:
            print(item['resourceName'], '已完成，跳过。')
