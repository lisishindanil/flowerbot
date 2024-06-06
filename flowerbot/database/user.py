from tortoise import Model, fields

class User(Model):
    id = fields.IntField(pk=True)
    uid = fields.IntField(null=False)
    city = fields.CharField(max_length=255, null=True)
    order = fields.JSONField(default=[])
    class Meta:
        table = 'users'
