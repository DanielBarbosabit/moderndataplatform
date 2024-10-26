from llama_index.agent.openai import OpenAIAgent
from llama_index.llms.openai import OpenAI
from os import getenv

class ChatbotAgentBuilder(object):
    def __init__(self, database_tools, logger):
        """
        Build the chatbot agent
        Refs:
            - https://docs.llamaindex.ai/en/stable/examples/llm/openai/
            - https://platform.openai.com/docs/models#gpt-4o-mini

        :param database_tools: Class to define database tools
        :param logger: Logger object
        """

        self.database_tools = database_tools
        self.llm_model = OpenAI(
                    model="gpt-4o-mini-2024-07-18",
                    api_key=getenv("OPENAI_API_KEY"),
                    temperature=0.8
        )
        self.agent = OpenAIAgent
        self.logger = logger

    def build(self):
        self.logger.info(f"""Available tools: {[tool.metadata.name for tool in self.database_tools]}""")
        return self.agent.from_tools(
            self.database_tools,
            system_prompt="Voce é um assistente que auxilia usuários a consultar informacoes em um banco de dados"
                          "postgres que voce possui acesso. Qualquer informacao que nao seja respondida pelos dados"
                          "do banco de dados, nao deverá ser respondido a usuario. Sempre responda em portugues",
            llm=self.llm_model,
            verbose=True
        )