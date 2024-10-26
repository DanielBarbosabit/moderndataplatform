import chainlit as cl
from integration.database.postgres.tool import DatabaseTool
from chatbot.src.agent.builder.agent import ChatbotAgentBuilder
from common.logger import Logger

logger = Logger("chatbot_logger").get_logger()

agent = ChatbotAgentBuilder(database_tools=DatabaseTool().build(),
                            logger=logger).build()

@cl.on_message
async def main(message: cl.Message):
    logger.info("New user message received")
    response = agent.chat(message.content)
    logger.info("Agent generated response")
    await cl.Message(
        content=f"{response}",
    ).send()
    logger.info("Response was sent to user")