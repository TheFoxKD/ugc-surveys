from typing import Any

from rest_framework import serializers

from src.surveys.models import AnswerOption, Question, Survey


class AnswerOptionNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = ("id", "text", "position")


class QuestionNestedSerializer(serializers.ModelSerializer):
    answer_options = AnswerOptionNestedSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ("id", "text", "position", "answer_options")


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ("id", "title", "created_at", "updated_at")


class SurveyCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ("title",)

    def create(self, validated_data: dict[str, Any]) -> Survey:
        author = self.context["author"]
        return Survey.objects.create(author=author, **validated_data)

    def update(self, instance: Survey, validated_data: dict[str, Any]) -> Survey:
        for field, value in validated_data.items():
            setattr(instance, field, value)
        if validated_data:
            instance.save(update_fields=[*validated_data.keys(), "updated_at"])
        return instance


class SurveyDetailSerializer(serializers.ModelSerializer):
    questions = QuestionNestedSerializer(many=True, read_only=True)

    class Meta:
        model = Survey
        fields = ("id", "title", "created_at", "updated_at", "questions")
