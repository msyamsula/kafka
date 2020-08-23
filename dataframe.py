from peewee import *
import pandas as pd
from peewee import *
from playhouse.db_url import connect

db = connect('mysql://root:agh765@V@localhost:3306/student_score')

class BaseModel(Model):
    class Meta:
        database = db

class students_result(BaseModel):
    CATEGORY_ID = IntegerField()
    SCORE = IntegerField()
    CATEGORY = CharField()
    ID = IntegerField(primary_key=True)
    STUDENT_ID = IntegerField()
    NAME = CharField()

a = list(students_result.select().execute())

for data in a:
    print(data, data.SCORE)