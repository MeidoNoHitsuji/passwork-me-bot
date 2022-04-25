import json
import re
from typing import Optional, Union
from regex import Match
import requests
from requests.cookies import RequestsCookieJar
from api import UserApi, WorkspaceApi
from configs import *

class PassworkClient:
    
    headers = dict()
    cookies: Optional[RequestsCookieJar] = None
    _id: Optional[int] = None
    workspace: str = None
    csrf: str = None
    private: str = None
    userApi = UserApi()
    
    def __init__(self, login, password, masterKey) -> None:
        response, self.cookies = self.userApi.authorize(login, password)
        self._id = response.get('id')
        self.workspace = response.get('setWorkspace')
        self.csrf = self.get_csrf()
    
        self.workspaceApi = WorkspaceApi(self.cookies, self.csrf, self.workspace)
        
        if not self.userApi.check_master_hash(masterKey):
            raise Exception('MasterKey exception!!')
        
        self.private = self.userApi.get_private_key()
    
    def get_csrf(self):
        response = requests.get(f"{URL}", cookies=self.cookies)
        
        if response.status_code != 200:
            raise Exception(response.content)
        
        data: Optional[Match[str]] = re.search(r"__csrf = '([a-zA-Z0-9]+)';", response.content.decode('utf-8'))
        
        if data is None:
            raise Exception("CSRF not found!")
        
        return data.groups()[0]

