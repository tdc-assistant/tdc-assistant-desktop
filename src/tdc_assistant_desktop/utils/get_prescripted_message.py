from typing import List

from random import randint, choice

OPENING_MESSAGES: List[str] = [
    "Hello! how are you today?",
    "Hello! How are you doing?",
    "Hello, how are you today?",
    "Hello, How are you doing?",
]

HOW_MAY_HELP_MESSAGES: List[str] = [
    "I am well! How may I help you?",
    "I am doing fine! what can I help you with today?",
    "Great! What would you like some help with?",
]

SHOW_ME_MESSAGES: List[str] = [
    "Can you show me what you're working on?",
    "Please show me what you would like help with",
    "Gotcha! Can you share what you have so far?",
]

QUERY_PROBLEMS_MESSAGES: List[str] = [
    "What problems are you running into?",
    "Can you tell me what problems you're facing?",
    "Please tell me some more about the issues that you're having",
]

PRESCRIPTED_MESSAGES: List[List[str]] = [
    OPENING_MESSAGES,
    HOW_MAY_HELP_MESSAGES,
    SHOW_ME_MESSAGES,
    QUERY_PROBLEMS_MESSAGES,
]


def get_prescripted_message(which: int):
    return choice(PRESCRIPTED_MESSAGES[which])
