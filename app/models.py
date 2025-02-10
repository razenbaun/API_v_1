from tortoise import fields, Tortoise
from tortoise.models import Model
from tortoise.signals import post_save, post_delete
from typing import Optional


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
    status = fields.CharField(max_length=50, default="")

    problems = fields.ReverseRelation["Problem"]


class User(Model):
    user_id = fields.IntField(pk=True)
    login = fields.CharField(max_length=50, unique=True)
    email = fields.CharField(max_length=40, unique=True)
    password = fields.CharField(max_length=255)
    admin = fields.BooleanField(default=False)

    problems = fields.ReverseRelation["Problem"]


class Problem(Model):
    problem_id = fields.IntField(pk=True)
    computer = fields.ForeignKeyField("models.Computer", related_name="problems")
    user = fields.ForeignKeyField("models.User", related_name="problems")
    description = fields.TextField()
    img = fields.TextField(null=True)
    active = fields.BooleanField(default=True)
    status = fields.CharField(max_length=50, default="Pending")


@post_save(Problem)
async def update_computer_status(model_class, instance, created, using_db, update_fields):
    computer = await instance.computer

    if instance.active:
        computer.status = instance.status
    else:
        active_problem = await Problem.filter(computer=computer, active=True).first()
        if active_problem:
            computer.status = active_problem.status
        else:
            computer.status = ""

    await computer.save()


@post_delete(Problem)
async def reset_computer_status(model_class, instance, using_db):
    computer = await instance.computer
    active_problem = await Problem.filter(computer=computer, active=True).first()

    if active_problem:
        computer.status = active_problem.status
    else:
        computer.status = ""

    await computer.save()
