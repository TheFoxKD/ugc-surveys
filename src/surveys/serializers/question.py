from typing import Any

from rest_framework import serializers

from src.surveys.models import AnswerOption, Question, Survey


class AnswerOptionNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = ("id", "text", "position")


class QuestionCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ("text", "position")

    def validate_position(self, value: int) -> int:
        survey: Survey | None = self.context.get("survey")
        if value <= 0:
            msg = "Позиция должна быть больше нуля"
            raise serializers.ValidationError(msg)
        if survey is None:
            msg = "Опрос не задан"
            raise serializers.ValidationError(msg)
        queryset = survey.questions.filter(position=value)
        if self.instance is not None:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            msg = "Вопрос с такой позицией уже существует"
            raise serializers.ValidationError(msg)
        return value

    def create(self, validated_data: dict[str, Any]) -> Question:
        survey: Survey = self.context["survey"]
        return survey.questions.create(**validated_data)

    def update(self, instance: Question, validated_data: dict[str, Any]) -> Question:
        for field, value in validated_data.items():
            setattr(instance, field, value)
        if validated_data:
            instance.save(update_fields=[*validated_data.keys(), "updated_at"])
        return instance


class QuestionNestedSerializer(serializers.ModelSerializer):
    answer_options = AnswerOptionNestedSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ("id", "text", "position", "answer_options")
