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

    places = fields.ReverseRelation["Place"]


class Place(Model):
    place_id = fields.IntField(pk=True)
    x = fields.IntField()
    y = fields.IntField()
    placeType = fields.CharField(max_length=50, default="standard")
    classroom = fields.ForeignKeyField("models.Classroom", related_name="places")

    devices = fields.ReverseRelation["Device"]


class Device(Model):
    device_id = fields.IntField(pk=True)
    place = fields.ForeignKeyField("models.Place", related_name="devices")
    status = fields.CharField(max_length=50, default="")
    description = fields.CharField(max_length=255, null=True)

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
    device = fields.ForeignKeyField("models.Device", related_name="problems")
    user = fields.ForeignKeyField("models.User", related_name="problems")
    description = fields.TextField()
    active = fields.BooleanField(default=True)
    status = fields.CharField(max_length=50, default="Pending")


@post_save(Problem)
async def update_device_status(model_class, instance, created, using_db, update_fields):
    device = await instance.device

    if instance.active:
        device.status = instance.status
    else:
        active_problem = await Problem.filter(device=device, active=True).first()
        if active_problem:
            device.status = active_problem.status
        else:
            device.status = ""

    await device.save()


@post_delete(Problem)
async def reset_device_status(model_class, instance, using_db):
    device = await instance.device
    active_problem = await Problem.filter(device=device, active=True).first()

    if active_problem:
        device.status = active_problem.status
    else:
        device.status = ""

    await device.save()
