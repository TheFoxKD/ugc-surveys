from rest_framework import serializers

from src.surveys.models import AnswerOption, Question


class AnswerOptionPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = ("id", "text", "position")


class QuestionPublicSerializer(serializers.ModelSerializer):
    answer_options = AnswerOptionPublicSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ("id", "text", "position", "answer_options")


class NextQuestionSerializer(serializers.Serializer):
    run_id = serializers.IntegerField()
    question = QuestionPublicSerializer()


class AnswerSubmitSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    option_id = serializers.IntegerField()


class AnswerResultSerializer(serializers.Serializer):
    """Ответ после отправки ответа пользователем.

    Возвращает идентификатор прогона, флаг завершённости и следующий вопрос,
    если он ещё есть. Это позволяет клиенту сразу понять, что делать дальше,
    без дополнительного запроса.
    """

    run_id = serializers.IntegerField()
    completed = serializers.BooleanField()
    question = QuestionPublicSerializer(required=False, allow_null=True)
