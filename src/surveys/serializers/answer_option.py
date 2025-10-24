from typing import Any

from rest_framework import serializers

from src.surveys.models import AnswerOption, Question


class AnswerOptionCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = ("text", "position")

    def validate_position(self, value: int) -> int:
        question: Question | None = self.context.get("question")
        if value <= 0:
            msg = "Позиция должна быть больше нуля"
            raise serializers.ValidationError(msg)
        if question is None:
            msg = "Вопрос не задан"
            raise serializers.ValidationError(msg)
        queryset = question.answer_options.filter(position=value)
        if self.instance is not None:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            msg = "Вариант с такой позицией уже существует"
            raise serializers.ValidationError(msg)
        return value

    def create(self, validated_data: dict[str, Any]) -> AnswerOption:
        question: Question = self.context["question"]
        return question.answer_options.create(**validated_data)

    def update(
        self,
        instance: AnswerOption,
        validated_data: dict[str, Any],
    ) -> AnswerOption:
        for field, value in validated_data.items():
            setattr(instance, field, value)
        if validated_data:
            instance.save(update_fields=[*validated_data.keys(), "updated_at"])
        return instance


class AnswerOptionNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = ("id", "text", "position")
