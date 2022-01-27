import motor.motor_asyncio
from montydb import MontyClient, set_storage
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError


class AutoDBClient:
    """
    Initialize a auto database.

    Parameters
    ----------
    `name` : str
        The name of the database.
    `use_motor` : bool
        Whether to use motor's asyncio. Defaults to False.
    `db_path` : str
        Path to the database if MontyClient will be used. Defaults to ./db. Only applicable to montydb.
    `connection_string` : str
        Connection string for mongodb. Only applicable to motor and pymongo.
    `connection_timeout` : int
        Timeout in ms for connecting to mongodb. Defaults to 10000. Only applicable to motor or pymongo.
    `cache_modified` : int
        Cache modified parameter for montydb. Defaults to 0. Only applicable to montydb.
    `logging` : Logging
        prettylog's Logging object. Defaults to None. If a logger is passed, every log coming from this library will be in the group "autodb"
    """

    def __init__(self, name: str, **kwargs) -> None:
        # Params
        self.use_motor = kwargs.get("use_motor", False)
        self.db_path = kwargs.get("db_path", "./db")
        self.connection_string = kwargs.get("connection_string")
        self.connection_timeout = kwargs.get("connection_timeout", 10000)
        self.cache_modified = kwargs.get("cache_modified", 0)
        self.logging = kwargs.get("logging")

        self.internal_client = None
        self.db = None
        self.type = "monty"

        if self.connection_string:
            try:
                if self.use_motor:
                    self.internal_client = motor.motor_asyncio.AsyncIOMotorClient(self.connection_string, serverSelectionTimeoutMS=self.connection_timeout)
                else:
                    self.internal_client = MongoClient(self.connection_string, serverSelectionTimeoutMS=self.connection_timeout)
                
                self.db = self.internal_client[name]

                if not self.use_motor:
                    self.internal_client.server_info()

                self.type = "mongo"
                if self.logging:
                    self.logging.success(f"Connected to mongodb using {self.connection_string}", group="autodb")
            except ServerSelectionTimeoutError:
                if self.logging:
                    self.logging.warning("Could not connect to mongodb. Falling back to montydb.", group="autodb")
        
        if self.type == "monty":
            try:
                set_storage(self.db_path, cache_modified=self.cache_modified)
                self.internal_client = MontyClient(self.db_path)
                self.db = self.internal_client[name]

                if self.logging:
                    self.logging.success(f"Successfully connected to montydb using the path {self.db_path}", group="autodb")

            except Exception as e:
                raise ConnectionError(f"Failed to connect to montydb. ({e})")
