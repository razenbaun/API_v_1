from tortoise import fields, Tortoise
from tortoise.models import Model

class Campus(Model):
    campus_id = fields.IntField(pk=True)
    campus_number = fields.IntField()
    address = fields.CharField(max_length=255)

    classrooms = fields.ReverseRelation["Classroom"]

class Classroom(Model):
    classroom_id = fields.IntField(pk=True)
    classroom_number = fields.IntField()
    campus = fields.ForeignKeyField("models.Campus", related_name="classrooms")

    computers = fields.ReverseRelation["Computer"]

class Computer(Model):
    computer_id = fields.IntField(pk=True)
    computer_ip = fields.CharField(max_length=15)
    classroom = fields.ForeignKeyField("models.Classroom", related_name="computers")

    problems = fields.ReverseRelation["Problem"]

class User(Model):
    user_id = fields.IntField(pk=True)
    login = fields.CharField(max_length=50, unique=True)
    password = fields.CharField(max_length=255)
    admin = fields.BooleanField(default=False)

    problems = fields.ReverseRelation["Problem"]

class Problem(Model):
    problem_id = fields.IntField(pk=True)
    computer = fields.ForeignKeyField("models.Computer", related_name="problems")
    user = fields.ForeignKeyField("models.User", related_name="problems")
    description = fields.TextField()
    img = fields.BinaryField(null=True)
    active = fields.BooleanField(default=True)
    status = fields.CharField(max_length=50, default="Pending")

async def init():
    await Tortoise.init(
        db_url="sqlite://db.sqlite3",
        modules={"models": [__name__]}
    )
    await Tortoise.generate_schemas()

if __name__ == "__main__":
    import asyncio
    asyncio.run(init())
