# -*- coding: utf-8 -*-
import datetime
import os
import peewee
from playhouse.shortcuts import model_to_dict


database_path = '/home/rrocha/projects/feagri/ebbandflow.db'
database = peewee.SqliteDatabase(database_path)


class BaseModel(peewee.Model):
    class Meta:
        database = database

    def to_dict(self, datefield_format='%d/%m/%Y'):
        dict_model = model_to_dict(self)

        for key, value in dict_model.items():
            if isinstance(value, datetime.date):
                new_value = value.strftime(datefield_format)
                dict_model[key] = new_value

        return dict_model


class PlantStatus(BaseModel):   

    operation_mode = peewee.CharField()
    substrate_humidity = peewee.CharField()
    solution_ph = peewee.CharField()
    substrate_humidity_pump = peewee.CharField()
    substrate_humidity_set_point = peewee.CharField()
    created_date = peewee.DateTimeField(default=datetime.datetime.now)
