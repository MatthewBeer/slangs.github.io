from tortoise import fields
from tortoise.models import Model

class Slang(Model):

    id = fields.IntField(pk=True)

    word = fields.TextField()
    description = fields.TextField()
    type = fields.TextField()

    created = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "words"
