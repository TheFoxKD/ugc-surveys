from __future__ import annotations

from django.core.management.base import BaseCommand

from src.surveys.services.demo_seed import DemoSeedService


class Command(BaseCommand):
    help = "Seed small demo dataset"

    def handle(self, *_args: object, **_options: object) -> None:
        result = DemoSeedService.seed()
        self.stdout.write(
            "\n".join(
                [
                    "Demo data seeded:",
                    f"  Author email: {result.author_email}",
                    f"  User email: {result.user_email}",
                    f"  Password: {result.password}",
                    f"  Survey id: {result.survey_id}",
                    f"  Questions created: {result.questions_created}",
                    f"  Options created: {result.options_created}",
                    f"  Run id: {result.run_id}",
                    f"  Answers created: {result.answers_created}",
                ],
            ),
        )
