# from langchain_community.chat_models import BedrockChat
# import boto3
from langchain_community.chat_models import ChatLiteLLM

# from langchain_community.embeddings import BedrockEmbeddings
import litellm

litellm.success_callback = ["langfuse"]


class Models:
    def claude3Haiku():
        return {
            "model": ChatLiteLLM(
                model="claude-3-haiku-20240307",
                max_tokens=4096,
            ),
            "max_rpm": 5,
            "max_iter": 15,
        }

    def bedrockHaiku():
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
                        "trace_user_id": "user-id15",  # set langfuse Trace User ID
                        "session_id": "session-15",  # set langfuse Session ID
                        "tags": ["tag1", "tag2"],
                    }
                },
            ),
            "max_rpm": 10,
            "max_iter": 15,
        }
