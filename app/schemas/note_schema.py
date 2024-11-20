from enum import Enum


class NoteTypeEnum(str, Enum):
    general = "general"
    definition = "definition"
    example = "example"
    question = "question"
    answer = "answer"
