from tortoise import Model, fields


class User(Model):
    id = fields.IntField(pk=True)
    uid = fields.IntField(null=False)
    city = fields.CharField(default="Kyiv", max_length=255, null=True)
    cart = fields.JSONField(default=[])
    order = fields.JSONField(default=[])

    class Meta:
        table = 'users'
