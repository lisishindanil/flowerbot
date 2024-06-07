from tortoise import Model, fields


class Catalog(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100, null=False)
    price = fields.FloatField(null=False)
    count = fields.IntField(null=False)
    image = fields.BinaryField(null=True)

    class Meta:
        table_name = 'catalog'
