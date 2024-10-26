from llama_index.tools.database.base import DatabaseToolSpec
from os import getenv


class DatabaseTool(object):
    def __init__(self):
        self.database_uri = getenv("DATABASE_URI")

    def build(self):
        """
        Build the tools to list and describe tables in the database and
        allow to execute query on it.
        :return: Tool list
        """
        database_spec = DatabaseToolSpec(uri=self.database_uri)
        return database_spec.to_tool_list()
