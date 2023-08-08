from dsapi import ApiProjectData, ApiProjectLimits, ApiProjectSettings
from sarov import SarovManager
from config import DefaultConfig
from dsapi import DsApi
from hackyapi import hackyDSApi
config = DefaultConfig()
dsapi = DsApi(config.token, config.org_id, community_id=config.community_id)

sarovm = SarovManager(dsapi, config)
# sarovm.update_user_projects_balances(999999999)

# sarovm.start_all_projects()

# sarovm.start_all_kernels()
sarovm.get_file_from_projects('PID_torch.onnx')

sarovm.get_file_from_projects('PID_sklearn.onnx')

#  sarovm.updateDefaultProjectsSettings()
# sarovm.start_all_projects()
# sarovm.stop_all_projects()
# sarovm.addDatasetToProjects('bt1n2n335chd62j1d6pb')
# sarovm.addDatasetToProjects('bt1v9gu03vq1dtgg0b3h')
# sarovm.create_projects_for_users()


hackyds = hackyDSApi(
    yandex_login=config.yandex_login,
    yc_session=config.yc_session,
    session_id=config.session_id,
    download_file_token=config.download_file_token
)

hackyds.start_kernel('bt1ub593tbin4gnb2h1a')

hackyds.get_operation_status('bt12i1mr81l8466l15o9')

# hackyds.startProject('bt185n17sk4ig8k42iqs')
file = hackyds.download_file('bt1e1bqt8kog1bpbj8nj', 'Untitled.ipynb')



sarovm.create_projects_for_users()
sarovm.update_user_roles()


# sarovm.addS3MountToProjects('bt1k4s6oa0tt988p1u3r') # sarov-share-readonly
# sarovm.addDockerImageToProjects('bt1cj66s01nk6bpk5q38')  # Docker image no gpu
# sarovm.addDockerImageToProjects('bt1q7jt5g91gjne7i929')  # Docker image gpu
# sarovm.addDatasetToProjects('bt1pvu8o253skoomc3f4')  # DATASET Seminar2


# sarovm.update_user_projects_balances(0)
# sarovm.updateDefaultProjectsSettings()
