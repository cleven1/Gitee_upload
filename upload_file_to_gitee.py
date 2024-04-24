import requests, json, hashlib, base64, logging, concurrent.futures
from datetime import datetime
 
# 设置全局变量，这里需要设置对应的 owner、repo 和 access_token
owner = "cleven_zhao"
access_token = ""
# 设置gitee仓库的用户名和密码
username = "cleven_zhao"
password = "heihei"
 
def read_file(file_path):
    """
    读取文件内容
    :param file_path: 文件路径
    :return: 文件内容
    """
    # 读取文件内容
    with open(file_path, "rb") as file:
        file_content = file.read()
    return file_content
 
def _push_gitee_file(gitee_file_path: str, repo_name: str):
    """
    将本地文件推送至 Gitee 仓库
    :param gitee_file_path: 文件在 Gitee 上的路径
    """
    file_name = gitee_file_path.split('/')[-1]
    url = f"https://gitee.com/api/v5/repos/{owner}/{repo_name}/contents/{file_name}"
    file_content = read_file(gitee_file_path)
    encoded_content = base64.b64encode(file_content).decode("utf-8")
    sha = sha = hashlib.sha1(file_content).hexdigest()
    message = f"Update {gitee_file_path} on {datetime.now()}"
 
    payload = {
        "access_token": access_token,
        "content": encoded_content,
        "sha": sha,
        "message": message,
        'path': file_name
    }
 
    headers = {
        'Content-Type': 'application/json;charset=UTF-8'
    }
 
    response = requests.post(url, json=payload, headers=headers, auth=(username, password))
    result = json.loads(response.text)
    logging.info(f'code == {response.status_code} content == {result}')
    if response.status_code == 201:
        content = result['content']
        download_url = content['download_url']
        size = content['size']
        sha = content['sha']
        return {'code': 200, 'download_url': download_url, 'size': size, 'sha': sha, 'repo_name': repo_name}
    else:
        return{'code': response.status_code, 'msg': result['message']}
    
def _delete_gitee_file(file_name: str, sha: str, repo_name: str):
    url = f"https://gitee.com/api/v5/repos/{owner}/{repo_name}/contents/{file_name}"
    payload = {
        "access_token": access_token,
        "sha": sha,
        "message": 'delete file',
        'path': file_name
    }
    headers = {
        'Content-Type': 'application/json;charset=UTF-8'
    }
    response = requests.delete(url, json=payload, headers=headers, auth=(username, password))
    result = json.loads(response.text)
    logging.info(f'code == {response.status_code} content == {result}')
    if response.status_code == 200:
        return {'code': response.status_code, 'msg': 'success'}
    return {'code': response.status_code, 'msg': result['message']}

def push_file_threaded(gitee_file_paths, repo_name: str):
    """多线程推送文件至 Gitee 仓库"""
    results = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(_push_gitee_file, gitee_file_path, repo_name) for gitee_file_path in gitee_file_paths]
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
    return results[0] if len(results) == 1 else results

def delete_file_threaded(filename, sha, repo_name):
    """多线程删除文件至 Gitee 仓库"""
    results = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(_delete_gitee_file, filename, sha, repo_name)]
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
    return results[0]
 

if __name__ == '__main__':
    # 调用示例
    file_path = "/Users/zhaoyongqiang/Downloads/d12a61a9-bc26-492e-93eb-fa53f98d5d9e.png"
    # results = push_file_threaded([file_path], repo_name='upload_file_1')
    # print(results)
    result = delete_file_threaded('d12a61a9-bc26-492e-93eb-fa53f98d5d9e.png', '002c3d5341b6781bcbcf6b874dffa826173912f8', 'upload_file_1')
    print(result)
