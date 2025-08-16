class DatabaseConfig:
    """Database configuration constants"""

    DEFAULT_HOST = 'localhost'
    DEFAULT_PORT = 3307
    DEFAULT_DATABASE = 'my_database'
    DEFAULT_USER = 'my_user'
    DEFAULT_PASSWORD = 'my_password'

    ENV_DB_HOST = 'DB_HOST'
    ENV_DB_PORT = 'DB_PORT'
    ENV_DB_NAME = 'DB_NAME'
    ENV_DB_USER = 'DB_USER'
    ENV_DB_PASSWORD = 'DB_PASSWORD'

    DEFAULT_CHARSET = 'utf8mb4'
    DEFAULT_ENGINE = 'InnoDB'
