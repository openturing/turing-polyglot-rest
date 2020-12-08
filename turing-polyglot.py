# coding: utf8
from __future__ import unicode_literals

import hug
from hug_middleware_cors import CORSMiddleware
from polyglot.text import Text
import re


@hug.post('/ent')
def ent(text: str, model: str):
    """Get entities for polyglot Entities."""

    emails = re.findall(r'[\w\.-]+@[\w\.-]+', text)

    polyglot_text = Text(text,  hint_language_code=model)

    places = []
    persons = []
    orgs = []
    for entity in polyglot_text.entities:
        if entity.tag == 'I-LOC':
            places.append(' '.join(entity))
        if entity.tag == 'I-PER':
            persons.append(' '.join(entity))
        if entity.tag == 'I-ORG':
            orgs.append(' '.join(entity))

    return [{'places': places, 'persons': persons, 'orgs': orgs, 'emails': emails}]


if __name__ == '__main__':
    app = hug.API(__name__)
    app.http.add_middleware(CORSMiddleware(app))
