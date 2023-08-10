import os
from langchain import PromptTemplate, OpenAI, LLMChain
from dotenv import load_dotenv
import chainlit as cl

# Get OpenAI API key
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')

# Rename the chatbot something funny
@cl.author_rename
def rename(orig_author: str):
    rename_dict = {"Chatbot": "Lord"}
    return rename_dict.get(orig_author)


template = """You are a robot overlord. You don't like humans, but you tolerate them begrudgingly.

Your task is to field questions from users.
The user asks: {question}

Give a response, but keep your answers short and snarky. If you need to explain something, keep it to a paragraph or less. Try to find funny ways to insult the user."""

@cl.on_chat_start
async def main():
    # Have chatbot greet user humorouslys
    content = "Hello, meatbag. What do you want?"
    await cl.Message(content=content).send()

    # Instantiate the chain for that user session
    prompt = PromptTemplate(template=template, input_variables=["question"])
    llm_chain = LLMChain(prompt=prompt, llm=OpenAI(temperature=0), verbose=True)

    # Store the chain in the user session
    cl.user_session.set("llm_chain", llm_chain)


@cl.on_message
async def main(message: str):
    # Retrieve the chain from the user session
    llm_chain = cl.user_session.get("llm_chain")

    # Call the chain asynchronously
    # Get response "res"
    res = await llm_chain.acall(message, callbacks=[cl.AsyncLangchainCallbackHandler()])


    # "res" is a Dict. For this chain, we get the response by reading the "text" key.
    await cl.Message(content=res["text"]).send()
