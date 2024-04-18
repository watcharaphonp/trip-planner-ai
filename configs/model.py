# from langchain_community.chat_models import BedrockChat
# import boto3
from langchain_community.chat_models import ChatLiteLLM

# from langchain_community.embeddings import BedrockEmbeddings
import litellm
import time

litellm.success_callback = ["langfuse"]


class Models:
    def gemini(user_id):
        return {
            "model": ChatLiteLLM(
                model="gemini/gemini-pro",
                model_kwargs={
                    "metadata": {
                        "trace_user_id": f"{user_id}",  # set langfuse Trace User ID
                        "session_id": f"{str(time.time())}-{user_id}",  # set langfuse Session ID
                        "tags": ["tag1", "tag2"],
                    }
                },
            ),
            "max_rpm": None,
            "max_iter": 15,
        }

    def claude3Haiku(user_id):
        return {
            "model": ChatLiteLLM(
                model="claude-3-haiku-20240307",
                max_tokens=4096,
                model_kwargs={
                    "metadata": {
                        "trace_user_id": f"{user_id}",  # set langfuse Trace User ID
                        "session_id": f"{str(time.time())}-{user_id}",  # set langfuse Session ID
                        "tags": ["tag1", "tag2"],
                    }
                },
            ),
            "max_rpm": 5,
            "max_iter": 15,
        }

    def bedrockHaiku(user_id):
        # bedrock_runtime = boto3.client(
        #     service_name="bedrock-runtime", region_name="us-east-1"
        # )
        model_id = "anthropic.claude-3-haiku-20240307-v1:0"

        return {
            # "model": BedrockChat(
            #     client=bedrock_runtime,
            #     model_id=model_id,
            #     model_kwargs={
            #         "max_tokens": 2048,
            #         "temperature": 0.1,
            #         "top_k": 250,
            #         "top_p": 1,
            #         "stop_sequences": ["\n\nHuman"],
            #     },
            # ),
            "model": ChatLiteLLM(
                model=model_id,
                max_tokens=2048,
                temperature=0.1,
                model_kwargs={
                    "metadata": {
                        "trace_user_id": f"{user_id}",  # set langfuse Trace User ID
                        "session_id": f"session-{user_id}",  # set langfuse Session ID
                        "tags": ["tag1", "tag2"],
                    }
                },
            ),
            "max_rpm": None,
            "max_iter": 15,
        }
