import openai
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

function_descriptions = [
    {
        "name": "extract_info_from_email",
        "description": "categorise & extract key info from an email, such as use case, company name, contact details, etc.",
        "parameters": {
            "type": "object",
            "properties": {
                "companyName": {
                    "type": "string",
                    "description": "the name of the company that sent the email"
                },                                        
                "summary": {
                    "type": "string",
                    "description": "Try to summarize the content of the email"

            },
            "required": ["companyName", "summary"]}
        }
    }
]


# email = """
# Dear Hitachi
# I hope this message finds you well. I'm Tom from Terna;
#
# I'm looking to purchase some STATCOMs for my plant, we want to cover 200MVAR of power
#
# Please let me know the price and timeline and the number of STATCOMs you can sell;
#
# Looking forward
#
# Tom
# """
#
# prompt = f"Please extract key information from this email: {email} "
# message = [{"role": "user", "content": prompt}]
#
# response = openai.ChatCompletion.create(
#     model="gpt-4-0613",
#     messages=message,
#     functions = function_descriptions,
#     function_call="auto"
# )
#
# print(response)




class Email(BaseModel):
    from_email: str
    content: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/")
def analyse_email(email: Email):
    content = email.content
    query = f"Please extract key information from this email: {content} "

    messages = [{"role": "user", "content": query}]

    response = openai.ChatCompletion.create(
        model="gpt-4-0613",
        messages=messages,
        functions = function_descriptions,
        function_call="auto"
    )

    arguments = response.choices[0]["message"]["function_call"]["arguments"]
    companyName = eval(arguments).get("companyName")
    summary = eval(arguments).get("summary")


    return {
        "companyName": companyName,
        "summary": summary
    }

