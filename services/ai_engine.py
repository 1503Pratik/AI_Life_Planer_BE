# # # # services/ai_engine.py

# # # from openai import OpenAI
# # # from config import settings

# # # class AIEngine:
# # #     """
# # #     AI Engine wrapper for generating smart responses
# # #     using GPT models (or any LLM API you connect).
# # #     """

# # #     def __init__(self):
# # #         self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

# # #     def generate_response(self, prompt: str, system_role: str = "assistant") -> str:
# # #         """
# # #         Generates AI output based on a prompt.
# # #         """

# # #         try:
# # #             response = self.client.chat.completions.create(
# # #                 model="gpt-4o-mini",
# # #                 messages=[
# # #                     {"role": "system", "content": system_role},
# # #                     {"role": "user", "content": prompt}
# # #                 ],
# # #                 max_tokens=300,
# # #                 temperature=0.8
# # #             )

# # #             return response.choices[0].message["content"]

# # #         except Exception as e:
# # #             print("AI Engine Error:", e)
# # #             return "Sorry, I couldn't process your request right now."

# # #     def analyze_task_priority(self, task_description: str) -> str:
# # #         """
# # #         Analyze how important or urgent a task is.
# # #         """

# # #         prompt = f"""
# # #         Analyze this task and classify into: HIGH, MEDIUM, LOW priority.
# # #         Task: {task_description}
# # #         """

# # #         return self.generate_response(prompt)

# # #     def suggest_daily_plan(self, tasks: list) -> str:
# # #         """
# # #         Generate a structured daily plan based on tasks.
# # #         """

# # #         prompt = f"""
# # #         Create a practical time-boxed daily schedule using the tasks:
# # #         {tasks}

# # #         Output in bullet points.
# # #         """

# # #         return self.generate_response(prompt)







# # # services/ai_engine.py

# # from openai import OpenAI
# # from config import settings

# # class AIEngine:
# #     """
# #     AI Engine wrapper for generating smart responses
# #     using GPT models (or any LLM API you connect).
# #     """

# #     def __init__(self):
# #         self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

# #     def generate_response(self, prompt: str, system_role: str = "assistant") -> str:
# #         """
# #         Generates AI output based on a prompt.
# #         """

# #         try:
# #             response = self.client.chat.completions.create(
# #                 model="gpt-4o-mini",
# #                 messages=[
# #                     {"role": "system", "content": system_role},
# #                     {"role": "user", "content": prompt}
# #                 ],
# #                 max_tokens=300,
# #                 temperature=0.8
# #             )

# #             return response.choices[0].message["content"]

# #         except Exception as e:
# #             print("AI Engine Error:", e)
# #             return "Sorry, I couldn't process your request right now."

# #     def analyze_task_priority(self, task_description: str) -> str:
# #         """
# #         Analyze how important or urgent a task is.
# #         """

# #         prompt = f"""
# #         Analyze this task and classify into: HIGH, MEDIUM, LOW priority.
# #         Task: {task_description}
# #         """

# #         return self.generate_response(prompt)

# #     def suggest_daily_plan(self, tasks: list) -> str:
# #         """
# #         Generate a structured daily plan based on tasks.
# #         """

# #         prompt = f"""
# #         Create a practical time-boxed daily schedule using the tasks:
# #         {tasks}

# #         Output in bullet points.
# #         """

# #         return self.generate_response(prompt)


# # # -----------------------------
# # # ADD THIS FUNCTION AT THE END
# # # -----------------------------

# # client = OpenAI(api_key=settings.OPENAI_API_KEY)

# # def process_user_query(query: str) -> str:
# #     """
# #     Wrapper function used by the /process route.
# #     """

# #     try:
# #         response = client.chat.completions.create(
# #             model="gpt-4o-mini",
# #             messages=[
# #                 {"role": "system", "content": "You are a helpful AI assistant."},
# #                 {"role": "user", "content": query}
# #             ],
# #             max_tokens=300,
# #             temperature=0.8
# #         )

# #         return response.choices[0].message["content"]

# #     except Exception as e:
# #         print("AI Engine Route Error:", e)
# #         return "Sorry, I couldn't process your request."








# # services/ai_engine.py

# from mistralai import Mistral
# from config import settings

# # Initialize Mistral client
# mistral_client = Mistral(api_key=settings.MISTRAL_API_KEY)

# class AIEngine:
#     """
#     AI Engine wrapper for generating smart responses using Mistral AI.
#     """

#     def __init__(self):
#         self.client = mistral_client

#     def generate_response(self, prompt: str, system_role: str = "assistant") -> str:
#         """
#         Generates AI output using Mistral models.
#         """
#         try:
#             response = self.client.chat.complete(
#                 model="mistral-small-latest",   # You can change the model
#                 messages=[
#                     {"role": "system", "content": system_role},
#                     {"role": "user", "content": prompt}
#                 ]
#             )

#             return response.choices[0].message["content"]

#         except Exception as e:
#             print("AI Engine Error:", e)
#             return "Sorry, I couldn't process your request right now."

#     def analyze_task_priority(self, task_description: str) -> str:
#         """
#         Analyze the priority of a task.
#         """
#         prompt = f"""
#         Analyze this task and classify into: HIGH, MEDIUM, LOW priority.
#         Task: {task_description}
#         """

#         return self.generate_response(prompt)

#     def suggest_daily_plan(self, tasks: list) -> str:
#         """
#         Generate a structured daily plan based on tasks.
#         """
#         prompt = f"""
#         Create a practical time-boxed daily schedule using the tasks:
#         {tasks}

#         Output in bullet points.
#         """

#         return self.generate_response(prompt)


# # ---------------------------------------
# # Function used by routes/ai.py endpoint
# # ---------------------------------------

# def process_user_query(query: str) -> str:
#     """
#     Simple wrapper for the /process endpoint.
#     """
#     try:
#         response = mistral_client.chat.complete(
#             model="mistral-small-latest",
#             messages=[
#                 {"role": "system", "content": "You are a helpful AI assistant."},
#                 {"role": "user", "content": query}
#             ]
#         )

#         return response.choices[0].message.content

#     except Exception as e:
#         print("AI Route Error:", e)
#         return "Sorry, I could not generate a response."





# services/ai_engine.py
from config import settings
from mistralai import Mistral

# Initialize Mistral client
mistral_client = Mistral(api_key=settings.MISTRAL_API_KEY)

class AIEngine:
    """
    AI wrapper using Mistral. Methods return plain strings.
    """

    def __init__(self):
        self.client = mistral_client

    def _call_chat(self, messages, model="mistral-small-latest", max_tokens=512):
        """
        Core call. Returns textual content or raises an exception.
        """
        resp = self.client.chat.complete(model=model, messages=messages, max_tokens=max_tokens)
        # Mistral SDK returns objects; use .message.content
        try:
            return resp.choices[0].message.content
        except Exception as e:
            # fallback to string conversion
            print("Mistral call parse error:", e)
            return str(resp)

    def generate_response(self, prompt: str, system_role: str = "You are a helpful assistant.") -> str:
        messages = [
            {"role": "system", "content": system_role},
            {"role": "user", "content": prompt}
        ]
        return self._call_chat(messages)

    def analyze_task_priority(self, task_description: str) -> str:
        prompt = f"Classify this task into HIGH, MEDIUM, or LOW priority and give a 1-sentence reason: {task_description}"
        return self.generate_response(prompt)

    def suggest_daily_plan(self, tasks: list) -> str:
        prompt = f"Create a time-boxed daily plan using the tasks: {tasks}. Return a short JSON array of steps with time ranges."
        return self.generate_response(prompt)

# convenience top-level function used by routes/ai.py
def process_user_query(query: str) -> str:
    """
    Simple wrapper for /ai/process route.
    """
    try:
        messages = [
            {"role": "system", "content": "You are a helpful assistant that converts user text into JSON commands when possible."},
            {"role": "user", "content": query}
        ]
        resp = mistral_client.chat.complete(model="mistral-small-latest", messages=messages, max_tokens=512)
        return resp.choices[0].message.content
    except Exception as e:
        print("AI Route Error:", e)
        return "Sorry, I could not generate a response."
