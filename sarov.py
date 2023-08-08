import time
from config import DefaultConfig
from dsapi import DsApi, ApiProjectData, ApiProjectLimits, ApiProjectSettings
from hackyapi import hackyDSApi

class SarovManager:
    def __init__(self, dsapi: DsApi, config: DefaultConfig) -> None:
        self.admin_id = config.admin_id
        self.community_id = config.community_id
        self.projects_service_account_id = config.projects_service_account_id
        self.maxUnitsPerHour = config.maxUnitsPerHour
        self.maxUnitsPerExecution = config.maxUnitsPerExecution
        self.unitBalance = config.unitBalance
        self.dsapi = dsapi
        self.config = config
        self.hackyds = hackyDSApi(
            yandex_login=config.yandex_login,
            yc_session=config.yc_session,
            session_id=config.session_id,
            download_file_token=config.download_file_token
        )

    def start_all_projects(self):
        projects = self.dsapi.get_projects()
        for project in projects:
            self.hackyds.startProject(project_id=project.get('id'))

    def start_all_kernels(self):
        projects = self.dsapi.get_projects()
        for project in projects:
            self.hackyds.start_kernel(project_id=project.get('id'))

    def stop_all_projects(self):
        projects = self.dsapi.get_projects()
        for project in projects:
            self.hackyds.stopProject(project_id=project.get('id'))

    def get_file_from_projects(self, filename):
        projects = self.dsapi.get_projects()
        for project in projects:
            if 'Participant' in project.get('name'):
                project_id = project.get('id')
                project_name = project.get('name')
                self.hackyds.download_file(project_id, filename)
                print(f"{project_name} downloading file {filename}")

    def update_user_projects_balances(self, balance=None):
        projects = self.dsapi.get_projects()
        balance = balance if balance is not None else self.unitBalance
        for project in projects:
            if 'Participant' in project.get('name'):
                project_id = project.get('id')
                project_name = project.get('name')
                self.dsapi.project_set_unit_balance(project.get('id'), balance)
                print(f"{project_name} Setting unit balance {balance}")

    def update_user_roles(self):
        all_users = self.dsapi.get_org_users()
        bindings = []
        for user in all_users:
            user_id = user.get('sub')
            user_name = user.get('name')
            email = user.get('email')
            role = 'datasphere.communities.admin' if (user_id in self.config.admin_ids) else 'datasphere.communities.viewer'
            bindings.append(
                {
                    "roleId": role,
                    "subject": {
                        "id": user_id,  # Необходимо указать ID администратора проекта
                        "type": "userAccount"
                    }}
            )
            print(f'Adding {email} {user_name} ({user_id}) as {role}')
        data = {}
        data['accessBindings'] = bindings
        res = self.dsapi.community_set_access_bindings(data=data)
        print('done')

    def create_projects_for_users(self, all_users=[]):
        if not all_users:
            all_users = self.dsapi.get_org_users()
        projects = self.dsapi.get_projects()

        existed_projects = {}
        for project in projects:
            uid = project.get('name', '').split(" ")
            if len(uid) > 1:
                existed_projects[uid[1]] = project
        projects = {}
        for user in all_users:
            user_id = user.get('sub')
            # if user_id != 'aje2eksvbn8u7v001ieq':
            #     continue
            newproject = ApiProjectData(
                name="Participant {}".format(user_id),
                communityId=self.community_id,
                description=f'{user.get("name")}`s workplace',
                settings=ApiProjectSettings(
                    serviceAccountId=self.projects_service_account_id,
                    staleExecTimeoutMode='ONE_HOUR'
                ),
                limits=ApiProjectLimits(
                    maxUnitsPerHour=self.maxUnitsPerHour,
                    maxUnitsPerExecution=self.maxUnitsPerExecution
                )
            )
            if user_id in existed_projects:
                print("skipping existed project {}".format(user_id))
                continue
                result = self.dsapi.get_projects(
                    self.community_id, name_pattern="Participant {}".format(user_id))[0]
                project_id = result['id']
                self.dsapi.project_update(project_id, newproject)
                self.addAllResources(project_id)
                print('project for {} already exists'.format(
                    user.get('email', '')))
            else:
                res = self.dsapi.project_create(newproject)
                time.sleep(5)
                project = self.dsapi.get_projects(
                    name_pattern="Participant {}".format(user_id))[0]
                project_id = project.get('id')
                self.addAllResources(project_id)
                print("Project for {} {} is created".format(
                    user_id, user.get('name', '')))


            # Добавляем себя в проект админом, пользователя с ролью developer и сервисный аккаунт.
            # Добавить себя админом необходимо, чтобы появилась возможность добавлять остальных
            data = {}
            data['accessBindings'] = [{
                "roleId": 'datasphere.community-projects.admin',
                "subject": {
                    "id": self.admin_id,  # Необходимо указать ID администратора проекта
                    "type": "userAccount"
                }},
                {
                "roleId": 'datasphere.community-projects.developer',
                "subject": {
                    "id": user_id,
                    "type": "userAccount"
                }}
            ]
            res = self.dsapi.project_set_access_bindings(project_id, data)
            # print("Admin and user were added to project {} with response: {}".format(
            #     project_id, res))

            # Устанавливаем совокупный баланс на проект

            res = self.dsapi.project_set_unit_balance(
                project_id, self.unitBalance)
            self.hackyds.updateProjectSettings(project_id)

    def addAllResources(self, project_id):
            sc,sc2 = self.addS3MountToProject(project_id=project_id, s3_id='bt1k4s6oa0tt988p1u3r') # sarov-share-readonly
            print(f'adding s3 mount to project {project_id} {sc} {sc2}')
            sc,sc2 = self.addDockerImageToProject(project_id=project_id, docker_image_id='bt1cj66s01nk6bpk5q38')  # Docker image no gpu
            print(f'adding docker image to project {project_id} {sc} {sc2}')
            sc,sc2 = self.addDockerImageToProject(project_id=project_id, docker_image_id='bt1q7jt5g91gjne7i929')  # Docker image gpu
            print(f'adding docekr image2 mount to project {project_id} {sc} {sc2}')
            sc,sc2 = self.addDatasetToProject(project_id=project_id, dataset_id='bt1pvu8o253skoomc3f4')  # DATASET Seminar2
            print(f'adding s3 dataset to project {project_id} {sc} {sc2}')
            sc,sc2 = self.addDatasetToProject(project_id=project_id, dataset_id='bt1n2n335chd62j1d6pb')  # DATASET Competitions
            print(f'adding s3 dataset to project {project_id} {sc} {sc2}')
            sc,sc2 = self.addDatasetToProject(project_id=project_id, dataset_id='bt1v9gu03vq1dtgg0b3h')  # DATASET Gans
            print(f'adding s3 dataset to project {project_id} {sc} {sc2}')



    def addS3MountToProject(self, project_id, s3_id):
        sc, result2 = self.hackyds.add_resource_to_project(
            project_id=project_id,
            resource_type='RESOURCE_TYPE_S3',
            resource_id=s3_id
        )
        sc2, result2 = self.hackyds.activateS3(
            project_id=project_id,
            s3_id=s3_id
        )
        # print(f"{project_id} Adding s3 share")
        return (sc, sc2)

    def addS3MountToProjects(self, s3_id: str = None):
        if s3_id is None:
            s3_id = self.config.s3_id
        projects = self.dsapi.get_projects()
        assert len(s3_id) > 0
        for project in projects:
            if 'Participant' in project.get('name'):
                project_id = project.get('id')
                project_name = project.get('name')
                sc, sc2 = self.adds3MountToProject(
                    project_id=project_id,
                    s3_id=s3_id
                )
                print(f"{project_name} Adding s3 share {sc} {sc2}")

    def addDockerImageToProject(self, project_id, docker_image_id):
        sc, result = self.hackyds.add_resource_to_project(
            project_id=project_id,
            resource_type='RESOURCE_TYPE_DOCKER_IMAGE',
            resource_id=docker_image_id
        )
        sc2, result2 = self.hackyds.activateDockerImage(
            project_id=project_id,
            docker_image_id=docker_image_id
        )
        return (sc, sc2)

    def addDockerImageToProjects(self, docker_image_id: str = None):
        if docker_image_id is None:
            docker_image_id = self.config.docker_image_id
        projects = self.dsapi.get_projects()
        assert len(docker_image_id) > 0
        for project in projects:
            if 'Participant' in project.get('name'):
                project_id = project.get('id')
                project_name = project.get('name')
                sc, sc2 = self.addDockerImageToProject(
                    project_id=project_id,
                    docker_image_id=docker_image_id
                )
                print(f"{project_name} Adding docker image {sc} {sc2}")

    def addDatasetToProject(self, project_id, dataset_id):
        sc, result = self.hackyds.add_resource_to_project(
            project_id=project_id,
            resource_type='RESOURCE_TYPE_DATASET',
            resource_id=dataset_id
        )
        sc2, result2 = self.hackyds.activateDataset(
            project_id=project_id,
            dataset_id=dataset_id
        )
        return (sc, sc2)

    def addDatasetToProjects(self, dataset_id: str = None):
        if dataset_id is None:
            dataset_id = self.config.dataset_id
        projects = self.dsapi.get_projects()
        assert len(dataset_id) > 0
        for project in projects:
            if 'Participant' in project.get('name'):
                project_id = project.get('id')
                project_name = project.get('name')
                sc, sc2 = self.addDatasetToProject(
                    project_id=project_id,
                    dataset_id=dataset_id
                )
                print(f"{project_name} Adding dataset {sc} {sc2}")

    def updateDefaultProjectsSettings(self):
        projects = self.dsapi.get_projects()
        for project in projects:
            if 'Participant' in project.get('name'):
                project_id = project.get('id')
                project_name = project.get('name')
                sc, result = self.hackyds.updateProjectSettings(project_id)
                print(f"{project_name} updating project default settings {sc}")
