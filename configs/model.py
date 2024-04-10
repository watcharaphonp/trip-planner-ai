from langchain_community.chat_models import BedrockChat
import boto3


class Models:
    def claude3Haiku():
        # Configure the model to use
        bedrock_runtime = boto3.client(
            service_name="bedrock-runtime", region_name="us-east-1"
        )
        model_id = "anthropic.claude-3-haiku-20240307-v1:0"
        model_kwargs = {
            "max_tokens": 2048,
            "temperature": 0.1,
            "top_k": 250,
            "top_p": 1,
            "stop_sequences": ["\n\nHuman"],
        }

        return {
            "model": BedrockChat(
                client=bedrock_runtime,
                model_id=model_id,
                model_kwargs=model_kwargs,
            ),
            "max_rpm": 5,
            "max_iter": 15,
        }
