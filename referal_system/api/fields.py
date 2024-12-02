from rest_framework import serializers


class PhoneNumberSerializerField(serializers.Field):
    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        from phonenumber_field.phonenumber import PhoneNumber
        return PhoneNumber.from_string(data)
