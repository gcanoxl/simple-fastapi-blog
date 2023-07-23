from config_default import configs

try:
    import config_override

    configs |= config_override.configs
except ImportError:
    pass

configs["db"][
    "url"
] = f"mysql+pymysql://{configs['db']['user']}:{configs['db']['password']}@{configs['db']['host']}:{configs['db']['port']}/{configs['db']['database']}?charset=utf8mb4"
