from rest_framework import serializers

from .models import Character, Hat


class HatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hat
        fields = ('id', 'color')


class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ('id', 'name', 'age', 'weight', 'human', 'hat')
    
    def validate(self, data):
        human = data['human']
        name = data['name']
        age = data['age']
        weight = data['weight']
        hat = data['hat']
        if not human and hat:
            raise serializers.ValidationError("If not human, no hat can be associated")
        if human and weight >= 80.0 and age < 10:
            raise serializers.ValidationError("A human weighing more than 80 kg must be more than 10 years old")
        if 'p' in name.lower() and hat.color == 'Y':
            raise serializers.ValidationError("Name contains p so hat cannot be yellow")
        return data
