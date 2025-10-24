from rest_framework import serializers


class AnswerOptionStatsSerializer(serializers.Serializer):
    option_id = serializers.IntegerField()
    text = serializers.CharField()
    answers_count = serializers.IntegerField()


class QuestionStatsSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    text = serializers.CharField()
    options = AnswerOptionStatsSerializer(many=True)
    top_option_id = serializers.IntegerField(allow_null=True)


class SurveyStatsSerializer(serializers.Serializer):
    total_runs = serializers.IntegerField()
    avg_duration_seconds = serializers.FloatField(allow_null=True)
    questions = QuestionStatsSerializer(many=True)
