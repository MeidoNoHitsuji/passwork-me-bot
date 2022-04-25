import hashlib
import json
from typing import Optional, Union
import requests
from requests.cookies import RequestsCookieJar
from configs import *

class DefaultApi:
    
    cookies: Optional[RequestsCookieJar] = None
    csrf: str = None
    workspace: str = None
    url: str = None    
    
    def __init__(self, cookies: RequestsCookieJar, csrf: str, workspace: str, url: str = None) -> None:
        self.cookies = cookies
        self.csrf = csrf
        self.workspace = workspace
        self.url = f"{URL}/{url}" if url is not None else URL
    
    def request(self, method, url: str, data: dict = {}):
        
        if self.csrf is not None:
            data.update({
                '__csrf': self.csrf
            })
        
        kwargs = dict()
        
        if self.cookies is not None:
            kwargs['cookies'] = self.cookies
        
        if method == "get":
            if len(data)>0:
                kwargs['params'] = data
            response = requests.get(f"{self.url}/{url}", **kwargs)
        elif method == "post":
            if len(data)>0:
                kwargs['data'] = data
            response = requests.post(f"{self.url}/{url}", **kwargs)
        elif method == "put":
            if len(data)>0:
                kwargs['data'] = data
            response = requests.put(f"{self.url}/{url}", **kwargs)
        elif method == "patch":
            if len(data)>0:
                kwargs['data'] = data
            response = requests.patch(f"{self.url}/{url}", **kwargs)
        else:
            raise Exception('Error method!!')
        
        if response.status_code != 200:
            raise Exception(response.content)
        
        data = json.loads(response.content)
        
        _response: Union[dict, bool] = data.get('response')
        
        if isinstance(_response, bool):
            raise Exception(data.get('errorMessage'))
        
        if self.cookies is None:
            self.cookies = response.cookies
        
        return _response
        
    def _get(self, url: str, data: dict = {}) -> dict:
        return self.request('get', url, data)
        
    def _post(self, url: str, data: dict = {}) -> dict:
        return self.request('post', url, data)
    
    def _put(self, url: str, data: dict = {}) -> dict:
        return self.request('put', url, data)
    
    def _patch(self, url: str, data: dict = {}) -> dict:
        return self.request('patch', url, data)

class UserApi(DefaultApi):
    
    def __init__(self, cookies: RequestsCookieJar = None, csrf: str = None, workspace: str = None) -> None:
        super().__init__(cookies, csrf, workspace, 'user')
        
    def authorize(self, login, password):
        return self._post('authorize', {
            "email": login,
            "password": password
        }), self.cookies
        
    def get_user_colors(self):
        return self._post('getUserColors')
    
    def get_info(self):
        return self._post('getInfo')
    
    def check_master_hash(self, masterKey: str) -> bool:
        
        data = {
            'workspaceId': self.workspace,
            'sha256': f"sha256:{hashlib.sha256(masterKey.encode()).hexdigest()}"
        }
        
        response = self._post('checkMasterHash', data)
        return response.get('result')
    
    def get_private_key(self) -> str:
        data = {
            'workspaceId': self.workspace
        }
        
        response = self._post('getPrivateKey', data)
        return response.get('privateCrypted')
        
        
class WorkspaceApi(DefaultApi):
    
    def __init__(self, cookies: RequestsCookieJar, csrf: str, workspace: str) -> None:
        super().__init__(cookies, csrf, workspace, 'workspace')
    
    def get_current_user_workspaces(self):
        return self._post('getCurrentUserWorkspaces')
    
    def get(self):
        
        data = {
            'workspaceId': self.workspace
        }
    
        return self._post('get', data)
    
class GroupsApi(DefaultApi):
    
    def __init__(self, cookies: RequestsCookieJar, csrf: str, workspace: str) -> None:
        super().__init__(cookies, csrf, workspace, 'groups')
        
    def get(self):
        
        data = {
            'workspaceId': self.workspace
        }
    
        return self._post('get', data)