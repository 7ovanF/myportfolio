from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Project, Skill, Experience

class ProjectSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()
    # Writable Skill field to add relationship; send as list of IDs.
    skill_slugs = serializers.SlugRelatedField(
                source="skills",
                queryset=Skill.objects.all(),
                many=True,
                allow_null=True,
                slug_field="title_slug"
            )

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "url",
            "thumbnail",
            "description",
            "skill_slugs",
            "star_count",
            "is_starred",
            "starred_by_names",
        ]
        read_only_fields = ["id"]


    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_description(self, value):
        return strip_tags(value)


    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.starred_by.all()

    def get_starred_by_names(self, obj):
        return [ user.username for user in obj.starred_by.all() ]

class ExperienceSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    class Meta:
        model = Experience
        fields = [
            "id",
            "title",
            "description",
            "category",
            "thumbnail",
            "started_at",
            "ended_at",
            "star_count",
            "is_starred",
            "starred_by_names",
        ]
        read_only_fields = ["id"]


    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_description(self, value):
        return strip_tags(value)

    # TODO: check if category needs validating


    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.starred_by.all()

    def get_starred_by_names(self, obj):
        return [ user.username for user in obj.starred_by.all() ]
