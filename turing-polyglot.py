# coding: utf8
from __future__ import unicode_literals

import hug
from hug_middleware_cors import CORSMiddleware
from polyglot.text import Text
import re
from nameparser import HumanName
import json

@hug.post('/ent')
def ent(text: str, model: str):
    """Get entities for polyglot Entities."""

    emails = re.findall(r'[\w\.-]+@[\w\.-]+', text)

    passport_regex = "[A-PR-WYa-pr-wy][1-9]\\d" + "\\s?\\d{4}[1-9]"
    passport_p = re.compile(passport_regex)

    passport = re.findall(passport_p, text)
    polyglot_text = Text(text,  hint_language_code=model)

    places = []
    persons = []
    names = []
    orgs = []
    for entity in polyglot_text.entities:
        if entity.tag == 'I-LOC':
            places.append(' '.join(entity))
        if entity.tag == 'I-PER':
            person = ' '.join(entity).replace(" .",".")
            persons.append(person)
            names.append(HumanName(person).as_dict())
        if entity.tag == 'I-ORG':
            orgs.append(' '.join(entity))

    return [{'places': places, 'persons': persons, 'orgs': orgs, 'emails': emails, 'passport': passport, 'names': names}]


if __name__ == '__main__':
    app = hug.API(__name__)
    app.http.add_middleware(CORSMiddleware(app))
