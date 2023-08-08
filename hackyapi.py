import requests
import os
import time


class hackyDSApi:
    def __init__(self, yandex_login, yc_session, session_id, download_file_token) -> None:
        self.yandex_login = yandex_login
        self.yc_session = yc_session
        self.Session_id = session_id

    def startProject(self, project_id):
        data = {
            'ideExecutionMode': "DEDICATED",
            'projectId': project_id
        }
        sc, result = self.make_request(
            url='https://datasphere.yandex.com/gateway/datasphere/openProject',
            data=data
        )
        operation_id = result.get("id")
        data = {
            'operationId': operation_id
        }
        # while 1==1:
        #     sc2, result2 = self.make_request(
        #         url='https://datasphere.yandex.com/gateway/datasphere/getOperation',
        #         data=data
        #     )
        #     print(result.get('metadata').get('status'))
        #     time.sleep(5)
        print(f'starting project {project_id}, operation id {operation_id}')
        return (sc, result)

    def stopProject(self, project_id):
        data = {
            'ideExecutionMode': "DEDICATED",
            'projectId': project_id
        }
        sc, result = self.make_request(
            url='https://datasphere.yandex.com/gateway/datasphere/stopProject',
            data=data
        )
        operation_id = result.get("id")
        data = {
            'operationId': operation_id
        }
        print(f'stopping project {project_id}, operation id {operation_id}')
        return (sc, result)

    def get_operation_status(self, operation_id):
        data = {
            'operationId': operation_id
        }
        sc, result = self.make_request(
            url='https://datasphere.yandex.com/gateway/datasphere/getOperation',
            data=data
        )
        print(result.get('metadata').get('status'))

    def download_file(self, project_id, file_path):
        session = requests.session()

        json_data = {
            'projectId': project_id,
            'ideExecutionMode': 'DEDICATED',
        }
        sc, response = self.make_request(
            url='https://datasphere.yandex.com/gateway/datasphere/openProject',
            data=json_data
        )

        if sc != 200:
            raise Exception("can`t open project")
        operation_id = response.get("id")
        data = {
            'operationId': operation_id
        }
        sc, response = self.make_request(
            url='https://datasphere.yandex.com/gateway/datasphere/getOperation',
            data=data
        )
        ott = response.get('response', {}).get('sessionToken')
        projectUrl = response.get('response', {}).get('projectUrl')
        data = {
            'ott': ott,
            'projectUrl': projectUrl
        }
        response = session.get(
            url=f'https://{project_id}.yds.yandexcloud.net/proxy',
            data=data
        )
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7',
            'Connection': 'keep-alive',
            'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryU4fFjC74N6NXXNZo',
            'DNT': '1',
            'Origin': f'https://{project_id}.yds.yandexcloud.net',
            'Referer': f'https://{project_id}.yds.yandexcloud.net/proxy',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
        }

        data = f'------WebKitFormBoundaryU4fFjC74N6NXXNZo\r\nContent-Disposition: form-data; name="ott"\r\n\r\n{ott}\r\n------WebKitFormBoundaryU4fFjC74N6NXXNZo--\r\n'

        response = session.post(
            f'https://{project_id}.yds.yandexcloud.net/lab/v2/{project_id}',
            headers=headers,
            data=data,
        )

        url = f'https://{project_id}.yds.yandexcloud.net/lab/v2/{project_id}/files/project/{file_path}'
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            f'Referer': 'https://{project_id}.yds.yandexcloud.net/lab/v2/{project_id}/lab/workspaces/auto-4?reset',
        }

        response = session.get(
            url,
            headers=headers,
            # cookies=cookies
        )
        filename = os.path.basename(file_path)
        if response.status_code == 200:
            print(f"fetching file for project: {project_id}")
            open(f'results/{project_id}_{filename}',
                 'wb').write(response.content)
        else:
            if response.status_code == 405:
                print(f'{project_id} is not running')
            print(response.status_code)
        # if response.status_code == 200:
        result_data = {}
        try:
            result_data = response.json()
        except Exception as e:
            pass
        # else:
        #     raise Exception(f"Got bad resultcode ({response.status_code}) calling url {url}")
        return (response.status_code, result_data)

    def start_kernel(self, project_id):
        session = requests.session()

        json_data = {
            'projectId': project_id,
            'ideExecutionMode': 'DEDICATED',
        }
        sc, response = self.make_request(
            url='https://datasphere.yandex.com/gateway/datasphere/openProject',
            data=json_data
        )

        if sc != 200:
            raise Exception("can`t open project")
        operation_id = response.get("id")
        data = {
            'operationId': operation_id
        }
        sc, response = self.make_request(
            url='https://datasphere.yandex.com/gateway/datasphere/getOperation',
            data=data
        )
        ott = response.get('response', {}).get('sessionToken')
        projectUrl = response.get('response', {}).get('projectUrl')
        data = {
            'ott': ott,
            'projectUrl': projectUrl
        }
        response = session.get(
            url=f'https://{project_id}.yds.yandexcloud.net/proxy',
            data=data
        )
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7',
            'Connection': 'keep-alive',
            'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryU4fFjC74N6NXXNZo',
            'DNT': '1',
            'Origin': f'https://{project_id}.yds.yandexcloud.net',
            'Referer': f'https://{project_id}.yds.yandexcloud.net/proxy',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
        }

        data = f'------WebKitFormBoundaryU4fFjC74N6NXXNZo\r\nContent-Disposition: form-data; name="ott"\r\n\r\n{ott}\r\n------WebKitFormBoundaryU4fFjC74N6NXXNZo--\r\n'

        response = session.post(
            f'https://{project_id}.yds.yandexcloud.net/lab/v2/{project_id}',
            headers=headers,
            data=data,
        )
        cookies_dict = session.cookies.get_dict()
        url = f'https://{project_id}.yds.yandexcloud.net/lab/v2/{project_id}/api/kernels'
        if not cookies_dict.get('_xsrf', False):
            print(f'Looks like project {project_id} is not running')
            return

        headers = {
            'X-Xsrftoken': cookies_dict.get('_xsrf',''),
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            f'Referer': 'https://{project_id}.yds.yandexcloud.net/lab/v2/{project_id}/lab/workspaces/auto-4?reset',
        }
        data = {
            'name': 'python3',
        }
        response = session.post(
            url,
            headers=headers,
            json=data
            # cookies=cookies
        )
        result_data = {}
        try:
            result_data = response.json()
        except Exception as e:
            print(e)
        print(result_data)
        # else:
        #     raise Exception(f"Got bad resultcode ({response.status_code}) calling url {url}")
        return (response.status_code, result_data)

    def make_request(self, url, data=None):
        cookies = {
            'yandex_login': self.yandex_login,
            'yc_session': self.yc_session,
            'Session_id': self.Session_id,
        }

        headers = {
            'authority': 'datasphere.yandex.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'ru',
            'content-type': 'application/json',
            'dnt': '1',
            'origin': 'https://datasphere.yandex.com',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'x-csrf-token': '46d937d96b5ee0eda2f9c80be22f31eb9819824f:1689922162',
        }

        json_data = data

        response = requests.post(
            url,
            cookies=cookies,
            headers=headers,
            json=json_data,
        )
        result_data = {}
        try:
            result_data = response.json()
        except Exception as e:
            pass
        return (response.status_code, result_data)

    def add_resource_to_project(self, project_id, resource_type, resource_id):
        data = {
            'projectId': project_id,
            'resourceType': resource_type,
            'resourceId': resource_id,
        }
        try:
            sc, data = self.make_request(
                url='https://datasphere.yandex.com/gateway/datasphere/addResourceToProject',
                data=data
            )
        except Exception as e:
            print(f"error request {e}")
        if sc not in [200, 500]:
            raise Exception('something went wrong adding resource')
        return (sc, data)

    def activateS3(self, project_id, s3_id, mount_mode="READ_ONLY"):
        data = {
            'projectId': project_id,
            's3Id': s3_id,
            's3MountMode': mount_mode
        }
        sc, data = self.make_request(
            url='https://datasphere.yandex.com/gateway/datasphere/activateS3',
            data=data
        )
        if sc not in [200, 500, 400]:
            raise Exception('something went wrong activating s3 resource')
        return (sc, data)

    def activateDockerImage(self, project_id, docker_image_id):
        data = {
            'dockerId': docker_image_id,
            'projectId': project_id,
        }
        sc, data = self.make_request(
            url='https://datasphere.yandex.com/gateway/datasphere/activateDocker',
            data=data
        )
        if sc not in [200, 500, 400]:
            raise Exception('something went wrong activating Docker resource')
        return (sc, data)

    def activateDataset(self, project_id, dataset_id):
        data = {
            'datasetId': dataset_id,
            'projectId': project_id,
        }
        sc, data = self.make_request(
            url='https://datasphere.yandex.com/gateway/datasphere/activateDataset',
            data=data
        )
        if sc not in [200, 500, 400, 504]:
            raise Exception('something went wrong activating Dataset resource')
        return (sc, data)

    def updateProjectSettings(self, project_id):
        data = {
            'settings': {
                'staleExecTimeoutMode': "ONE_HOUR",
                'vmInactivityTimeout': {'seconds': "1800"}  # 30 min
            },
            'projectId': project_id,
            'updateMask': {
                'paths': ["settings.stale_exec_timeout_mode", "settings.vm_inactivity_timeout"]
            }
        }
        sc, result_data = self.make_request(
            url='https://datasphere.yandex.com/gateway/datasphere/updateProject',
            data=data
        )
        if sc not in [200, 500, 400]:
            raise Exception('something went wrong activating Dataset resource')
        return (sc, result_data)
