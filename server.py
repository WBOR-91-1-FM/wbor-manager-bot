from fastapi import FastAPI
from lists import profanity_list, ignored_words

tags_metadata = [
    {
        "name": "lists",
        "description": "Interacts with the lists managed by the bot. Currently, there are two lists: profanity and ignored_words.",
    }
]

app = FastAPI(openapi_tags=tags_metadata)

"""
Returns the list of words in the specified list, JSON-formatted.
"""


@app.get("/list/{name}", tags=["lists"])
async def read_list(name: str):
    if name == "profanity":
        return profanity_list.to_array()
    elif name == "ignored_words":
        return ignored_words.to_array()
    else:
        return {"error": "List not found."}
