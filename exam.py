from dataclasses import dataclass
from fastapi import FastAPI, HTTPException
from datetime import datetime as dt


app = FastAPI()

notes = []
next_id = 1


@dataclass
class Token:
    id: int
    text: str
    tags: list[str]
    created_at: dt


def text_is_correct(text):
    if not isinstance(text, str):
        raise HTTPException(400)
    if not text or len(text) > 200:
        raise HTTPException(400)


def tags_is_correct(tags):
    if tags is None:
        tags = []
    elif not isinstance(tags, list):
        raise HTTPException(400)
    elif len(tags) > 5:
        raise HTTPException(400)
    else:
        for tag in tags:
            if not isinstance(tag, str) or not tag or len(tag) > 20:
                raise HTTPException(400)

    return tags


@app.post("/notes", status_code=201)
def create_note(body: dict):
    global next_id

    text = body.get("text")
    tags = body.get("tags")

    text_is_correct(text)

    tags = tags_is_correct(tags)

    note = {"id": next_id, "text": text, "tags": tags, "created_at": dt.utcnow()}

    notes.append(note)
    next_id += 1
    return note


@app.get("/notes")
def get_notes(tag=None):
    if tag is None:
        return notes
    return [n for n in notes if tag in n["tags"]]


@app.patch("/notes/{id}")
def update_note(id: int, body: dict):
    for note in notes:
        if note["id"] == id:
            if "text" in body:
                text_is_correct(body["text"])
                note["text"] = body["text"]
            if "tags" in body:
                note["tags"] = tags_is_correct(body["tags"])
            return note
    raise HTTPException(404)


@app.delete("/notes/{id}", status_code=204)
def delete_note(id: int):
    for i, note in enumerate(notes):
        if note["id"] == id:
            notes.pop(i)
            return
    raise HTTPException(404)
