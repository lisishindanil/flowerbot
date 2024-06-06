from tortoise import Model, fields


class Flower(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100, null=False)
    price = fields.FloatField(null=False)
    count = fields.IntField(null=False)
    class Meta:
        table_name = 'flowers'
