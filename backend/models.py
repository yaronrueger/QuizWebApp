from pydantic import BaseModel, Field
from typing import List
from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator

###########################
##  Pydantic for posts   ##
###########################

class Question_Pydantic(BaseModel):
    title:      str     = Field(title="Question Title", min_length = 1)
    answers:  List[str] = Field(title="Liste der Antwortmöglichkeiten", min_length = 1, min_items = 4, max_items=4)
    points:     int     = Field(title="So viele Punkte gibt die Frage")

class Quiz_Pydantic(BaseModel):
    title:      str     = Field(title="Der Titel des Quiz", min_length = 1)
    desc:       str     = Field(title="Die Beschreibung des Quiz", min_length = 1)
    category:   int     = Field(title="Die ID der Kategorie")
    questions: List[Question_Pydantic] = Field(title="Questions lolol") # als String, so wartet pydantic, bis die Klasse später deklariert wird

class Answer_Pydantic(BaseModel): # Braucht kein tortoise model, wird ja nicht in der db gespeichert
    question:   int     = Field(title="Die ID der zugehörigen Question")
    chosen:     int     = Field(title="welche Antwortmöglichkeit gewählt wurde")

###########################
## Tortoise for Database ##
###########################

class Quiz_Tortoise(Model):
    id = fields.IntField(pk=True,unique=True)
    creator = fields.IntField()
    title = fields.CharField(max_length=255)
    desc = fields.TextField()
    category = fields.IntField()
    created = fields.DateField()
    modified = fields.DateField()
    plays = fields.IntField()
    class Meta:
        table = "quiz"

Quiz_Tortoise_Pydantic = pydantic_model_creator(Quiz_Tortoise, name="Quiz_Tortoise_Pydantic")

class Question_Tortoise(Model):
    id = fields.IntField(pk=True,unique=True)
    quiz_id = fields.IntField()
    title = fields.CharField(max_length=255)
    answers = fields.JSONField()
    points = fields.IntField()
    class Meta:
        table = "question"

class Rating_Tortoise(Model):
    id = fields.IntField(pk=True,unique=True)
    user = fields.IntField()
    question = fields.IntField()
    points = fields.IntField()
