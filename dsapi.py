import requests
from dataclasses import dataclass, asdict


@dataclass
class ApiProjectSettings:
    serviceAccountId: str = None
    subnetId: str = None
    dataProcClusterId: str = None
    commitMode: str = None
    securityGroupIds: list[str] = None
    staleExecTimeoutMode: str = None

    def dict(self):
        return {k: str(v) for k, v in asdict(self).items() if v is not None}


@dataclass
class ApiProjectLimits:
    maxUnitsPerHour: int = None
    maxUnitsPerExecution: int = None

    def dict(self):
        return {k: str(v) for k, v in asdict(self).items() if v is not None}


@dataclass
class ApiProjectData:
    communityId: str = None
    name: str = None
    description: str = None
    settings: ApiProjectSettings = None
    earlyAccess: bool = None
    ide: str = None
    defaultFolderId: str = None
    staleExecTimeoutMode: str = None
    limits: ApiProjectLimits = None

    def dict(self):
        return {k: str(v) if not isinstance(v, (ApiProjectSettings, ApiProjectLimits)) else v.dict() for k, v in vars(self).items() if v is not None}


class DsApi():
    def __init__(self, token, org_id, community_id=None) -> None:
        self.token = token
        self.org_id = org_id
        self.community_id = community_id

    def make_request(self, url, method='GET', data=None, headers=None):
        headers = {"Authorization": "Bearer {}".format(self.token)}
        if method == 'GET':
            response = requests.get(
                url,
                json=data,
                headers=headers
            )
        if method == "POST":
            response = requests.post(
                url,
                json=data,
                headers=headers
            )
        if method == "PATCH":
            response = requests.patch(
                url,
                json=data,
                headers=headers
            )
        if response.status_code == 200:
            data = response.json()
        else:
            raise Exception(f"Got bad resultcode ({response.status_code}) calling url {url}")
        return (response.status_code, data)

    def get_org_users(self):
        sc, res = self.make_request(
            url="https://organization-manager.api.cloud.yandex.net/organization-manager/v1/organizations/{}/users".format(self.org_id),              
        )
        result = res.get('users', {})
        all_users = []
        for user in result:
            all_users.append(user.get('subjectClaims'))
        return all_users

    def get_projects(self, community_id=None, name_pattern=None, owner_id=None):
        data = {}
        data['community_id'] = community_id if community_id is not None else self.community_id
        if name_pattern is not None:
            data['projectNamePattern'] = name_pattern
        if owner_id is not None:
            data['ownedById'] = owner_id

        sc, res = self.make_request(
            url="https://datasphere.api.cloud.yandex.net/datasphere/v2/projects",
            data=data
        )
        if sc != 200:
            raise Exception(f"get_projects result code {sc}")
        return res.get('projects', {})

    def project_create(self, project: ApiProjectData):
        data = project.dict()
        if 'communityId' not in data:
            data['communityId'] = self.community_id
        sc, res = self.make_request(
            url='https://datasphere.api.cloud.yandex.net/datasphere/v2/projects',
            method='POST',
            data=data)
        return res

    def project_update(self, project_id, project: ApiProjectData):
        data = project.dict()
        fields = []
        for key, value in data.items():
            if value is not None:
                fields.append(key)
        fields = ','.join(fields)
        data['updateMask'] = fields
        sc, res = self.make_request(
            method='PATCH',
            url=f'https://datasphere.api.cloud.yandex.net/datasphere/v2/projects/{project_id}',
            data=data)
        return res

    def project_set_access_bindings(self, project_id, data):
        sc, res = self.make_request(
            url='https://datasphere.api.cloud.yandex.net/datasphere/v2/projects/{}:setAccessBindings'.format(project_id),
            method='POST',
            data=data
        )
        return res

    def project_set_unit_balance(self, project_id, unit_balance=None):
        data = {}
        if unit_balance is not None:
            data["unitBalance"] = unit_balance
        sc, res = self.make_request(
            url='https://datasphere.api.cloud.yandex.net/datasphere/v2/projects/{}:unitBalance'.format(project_id),
            method='POST',
            data=data
        )
        return res

    def community_set_access_bindings(self, data, community_id=None):
        if community_id is None:
            community_id = self.community_id
        sc, res = self.make_request(
            url='https://datasphere.api.cloud.yandex.net/datasphere/v2/communities/{}:setAccessBindings'.format(community_id),
            method='POST',
            data=data
        )
        return res

    def community_get_access_bindings(self, community_id=None):
        if community_id is None:
            community_id = self.community_id
        sc, res = self.make_request(
            url=f'https://datasphere.api.cloud.yandex.net/datasphere/v2/communities/{community_id}:accessBindings',
            method='GET',
        )
        return res.get('accessBindings', [])

    def executeProject(self, project_id):
        sc, res = self.make_request(
            url=f'https://datasphere.api.cloud.yandex.net/datasphere/v2/projects/{project_id}:execute',
            method='POST',
        )
        return res