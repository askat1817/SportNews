from rest_framework import serializers

from main.models import Types, Post


class TypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Types
        fields = ('title', 'image',)

    def validate(self, title):
        if self.Meta.model.objects.filter(title=title).exist():
            raise serializers.ValidationError('заголовок не может повторяься')
        return title


# Form и ModelForm -> ModelForm(Form)
# serializer.Serializer


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('__all__')

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        post = Post.objects.create(author=user, **validated_data)
        return post

    def get_fields(self):
        action = self.context.get('action')
        fields = super().get_fields()
        if action == 'list':
            fields.pop('text')
            fields.pop('tags')
            fields.pop('category')
            fields.pop('created_at')
        elif action == 'create':
            fields.pop('slug')
            fields.pop('author')
        return fields


