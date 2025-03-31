from django.core.management.base import BaseCommand
from drf_spectacular.generators import SchemaGenerator
from drf_spectacular.renderers import OpenApiYamlRenderer
import os


class Command(BaseCommand):
    help = "Генерирует документацию API с помощью drf-spectacular"

    def add_arguments(self, parser):
        parser.add_argument(
            "--output",
            type=str,
            default="docs/schema.yaml",
            help="Путь к файлу, куда будет сохранена документация",
        )

    def handle(self, *args, **options):
        output_path = options["output"]
        self.stdout.write("Генерация схемы API...")

        generator = SchemaGenerator()
        schema = generator.get_schema(request=None, public=True)
        if schema is None:
            self.stderr.write("Ошибка: не удалось сгенерировать схему API.")
            return
        renderer = OpenApiYamlRenderer()
        rendered_schema = renderer.render(schema)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(
                rendered_schema.decode("utf-8")
                if isinstance(rendered_schema, bytes)
                else rendered_schema
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Документация успешно сохранена по адресу: {output_path}"
            )
        )
