import requests, json, logging

access_token = ''
repo_description = '文件仓库文件仓库文件仓库'
# 设置gitee仓库的用户名和密码
username = "cleven_zhao"
password = "heihei"

def create_gitee_repo(repo_name: str):
    if repo_name == None or len(repo_name) <= 0:
        return {'code': 400, 'msg': '仓库名不能为空'}

    headers = {'Content-Type': 'application/json;charset=UTF-8'}
    data = {
        'access_token': access_token,
        'name': repo_name,
        'description': repo_description,
        'auto_init': True,
        'private': True
    }
    url = 'https://gitee.com/api/v5/user/repos'

    response = requests.post(url, headers=headers, json=data, auth=(username, password))
    result = json.loads(response.text)
    logging.info(f'code == {response.status_code} content == {result}')
    if response.status_code == 201:
        return {'code': 200, 'msg': 'success'}
    else:
        return {'code': response.status_code, 'msg': result['message']}
    

if __name__ == '__main__':
    create_gitee_repo('upload_file_1')
