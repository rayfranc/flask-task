from marshmallow import fields, Schema


class TrimmedString(fields.String):
    def _deserialize(self, value, *args, **kwargs):
        if hasattr(value, 'strip'):
            value = value.strip()
        return super()._deserialize(value, *args, **kwargs)
