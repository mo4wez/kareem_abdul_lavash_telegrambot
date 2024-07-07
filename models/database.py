from peewee import SqliteDatabase, Model, IntegerField, CharField, DateTimeField, ForeignKeyField
import datetime

db = SqliteDatabase(r'C:\Users\moawe\Desktop\bakery_accounting\db\dbbakery.db')

class BaseModel(Model):
    class Meta:
        database = db

class Inventory(BaseModel):
    date_received = DateTimeField(default=datetime.datetime.now)
    bags_received = IntegerField()
    bags_remaining = IntegerField()

class BagUsage(BaseModel):
    inventory = ForeignKeyField(Inventory, backref='usages')
    type = CharField()  # 'bake', 'shopkeeper', 'needy', 'sold'
    amount = IntegerField()
    name = CharField(null=True)
    phone = CharField(null=True)
    date = DateTimeField(default=datetime.datetime.now)

db.connect()
db.create_tables([Inventory, BagUsage])
