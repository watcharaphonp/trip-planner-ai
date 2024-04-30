from langchain_community.chat_models import ChatLiteLLM
import litellm

litellm.success_callback = ["langfuse"]


class Models:
    def gemini(user_id, session_id):
        return {
            "model": ChatLiteLLM(
                model="gemini/gemini-pro",
                model_kwargs={
                    "metadata": {
                        "trace_user_id": f"{user_id}",
                        "session_id": f"{session_id}",
                        "tags": ["tag1", "tag2"],
                    }
                },
            ),
            "max_rpm": None,
            "max_iter": 15,
        }

    def claude3Haiku(user_id, session_id):
        return {
            "model": ChatLiteLLM(
                model="claude-3-haiku-20240307",
                max_tokens=4096,
                model_kwargs={
                    "metadata": {
                        "trace_user_id": f"{user_id}",
                        "session_id": f"{session_id}",
                        "tags": ["tag1", "tag2"],
                    }
                },
            ),
            "max_rpm": 5,
            "max_iter": 15,
        }

    def bedrockHaiku(user_id, session_id):
        model_id = "anthropic.claude-3-haiku-20240307-v1:0"
        return {
            "model": ChatLiteLLM(
                model=model_id,
                max_tokens=2048,
                temperature=0.1,
                model_kwargs={
                    "metadata": {
                        "trace_user_id": f"{user_id}",
                        "session_id": f"{session_id}",
                        "tags": ["tag1", "tag2"],
                    }
                },
            ),
            "max_rpm": None,
            "max_iter": 15,
        }
