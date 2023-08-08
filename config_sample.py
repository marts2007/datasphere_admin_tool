class DefaultConfig:
    token = ''
    org_id = ''
    community_id = ''
    admin_id = ''
    projects_service_account_id = ''
    admin_ids = [
        'ajenn0clbblfn2a028qt',  # marts2007
    ]
    # g2.mig (4 vCPU, 1/8 GPU A100)	18 unit / s
    # maxUnitsPerHour = 18 * 60 * 60       # g2.mig 1h
    # maxUnitsPerExecution = 18 * 60 * 20  # g2.mig 20 min
    # unitBalance = 18 * 60 * 60 * 20      # g2.mig 20 hours



    # g1.1 (8 vCPU, 1 GPU V100)    72 unit /s 
    maxUnitsPerHour = 72 * 60 * 60       # g2.mig 1h
    maxUnitsPerExecution = 72 * 60 * 20  # g2.mig 20 min
    unitBalance = 72 * 60 * 60 * 20      # g2.mig 20 hours


    # yandex hacky ds api (emulate browser calls)
    yandex_login = 'marts2007'
    yc_session = ''
    session_id = ''
    download_file_token = ''
    s3_id = ''  # id of s3 mount adapter
    docker_image_id = ''  # docker image id