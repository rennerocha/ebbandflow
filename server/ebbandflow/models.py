import datetime
import os
import peewee
from playhouse.shortcuts import model_to_dict


database_path = "/home/rrocha/projects/feagri/server/ebbandflow.db"
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


class StatusPlanta(BaseModel):   
    status_bomba = peewee.CharField()
    modo_operacao = peewee.CharField()
    umidade_set_point = peewee.CharField()
    intervalo_leitura = peewee.CharField()
    umidade_substrato = peewee.CharField()
    ph_solucao = peewee.CharField()
    ph_set_point = peewee.CharField()
    created_date = peewee.DateTimeField(default=datetime.datetime.now)


database.connect()
database.create_tables([StatusPlanta, ], True)

