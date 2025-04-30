import os
import csv
import requests

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from content.models import (
    AboutUsVideo,
    Gratitude,
    Review,
    Partner,
    TargetedFundraising,
    FundraisingPhoto,
    FundraisingTextBlock,
)
from content.models.targeted_fundraisings import FundraisingStatus


class Command(BaseCommand):
    help = "Импорт данных из TXT-файлов в базу данных"

    def handle(self, *args, **kwargs):
        base_url = "https://rassvet-apc.ru/"
        base_path = "data/"

        with open(
            os.path.join(base_path, "video.txt"), "r", encoding="utf-8"
        ) as f:
            reader = csv.DictReader(f, delimiter="\t")
            for row in reader:
                AboutUsVideo.objects.update_or_create(
                    title=row["title"],
                    url=row["url"],
                )

        with open(
            os.path.join(base_path, "gratitudes.txt"), "r", encoding="utf-8"
        ) as f:
            reader = csv.DictReader(f, delimiter="\t")
            for row_num, row in enumerate(reader, 1):
                if not row.get("file"):
                    continue
                relative_path = row["file"].lstrip("\\/")
                file_url = f"{base_url}{relative_path}"
                file_name = os.path.basename(relative_path)
                try:
                    title = row.get("title") or f"Благодарность #{row_num}"
                    file_basename = os.path.splitext(
                        os.path.basename(relative_path)
                    )[0]
                    existing_gratitudes = Gratitude.objects.filter(
                        file__contains=file_basename
                    )
                    existing_gratitude = None
                    for gratitude in existing_gratitudes:
                        if row["order"] == gratitude.order:
                            existing_gratitude = gratitude
                            break
                    if not existing_gratitude and row.get("order"):
                        existing_by_order = Gratitude.objects.filter(
                            order=row["order"]
                        ).first()
                        if existing_by_order:
                            existing_gratitude = existing_by_order
                    if existing_gratitude:
                        existing_gratitude.title = title
                        existing_gratitude.order = row["order"]
                        existing_gratitude.is_active = True
                        existing_gratitude.save()
                        self.stdout.write(
                            self.style.SUCCESS(
                                "Обновлена существующая благодарность: "
                                f"{file_url}"
                            )
                        )
                    else:
                        response = requests.get(file_url, timeout=10)
                        response.raise_for_status()
                        gratitude = Gratitude(
                            file=relative_path,
                            title=title,
                            order=row["order"],
                            is_active=True,
                        )
                        gratitude.save()
                        gratitude.file.save(
                            file_name, ContentFile(response.content), save=True
                        )
                        self.stdout.write(
                            self.style.SUCCESS(
                                "Успешно загружена новая благодарность: "
                                f"{file_url}"
                            )
                        )
                except requests.exceptions.RequestException as e:
                    self.stdout.write(
                        self.style.ERROR(
                            f"Ошибка загрузки {file_url}: {str(e)}"
                        )
                    )
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Ошибка: {str(e)}"))

        with open(
            os.path.join(base_path, "reviews.txt"), "r", encoding="utf-8"
        ) as f:
            reader = csv.DictReader(f, delimiter="\t")
            for row in reader:
                Review.objects.update_or_create(
                    author_name=row["author_name"],
                    defaults={
                        "content": row["content"],
                        "order": row["order"],
                        "is_active": row["is_active"] == "да",
                    },
                )

        with open(
            os.path.join(base_path, "partners.txt"), "r", encoding="utf-8"
        ) as f:
            reader = csv.DictReader(f, delimiter="\t")
            for row_num, row in enumerate(reader, 1):
                if not row.get("logo"):
                    continue
                relative_path = row["logo"].lstrip("\\/")
                logo_url = f"{base_url}{relative_path}"
                logo_filename = os.path.basename(relative_path)
                try:
                    name = row["name"]
                    logo_basename = os.path.splitext(
                        os.path.basename(relative_path)
                    )[0]
                    existing_partners = Partner.objects.filter(
                        logo__contains=logo_basename
                    )
                    existing_partner = None
                    for partner in existing_partners:
                        if partner.name == name:
                            existing_partner = partner
                            break
                    if not existing_partner:
                        existing_partner = Partner.objects.filter(
                            name=name
                        ).first()
                    if existing_partner:
                        existing_partner.description = row["description"]
                        existing_partner.order = row.get("order", 0)
                        existing_partner.save()

                        self.stdout.write(
                            self.style.SUCCESS(
                                f"Обновлен существующий партнер (ID: "
                                f"{existing_partner.id}): {name}"
                            )
                        )
                    else:
                        response = requests.get(logo_url, timeout=10)
                        response.raise_for_status()
                        partner = Partner(
                            name=name,
                            description=row["description"],
                            order=row.get("order", 0),
                        )
                        partner.save()
                        partner.logo.save(
                            logo_filename,
                            ContentFile(response.content),
                            save=True,
                        )
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"Создан новый партнер (ID: {partner.id}): "
                                f"{name} с логотипом: {logo_url}"
                            )
                        )
                except requests.exceptions.RequestException as e:
                    self.stdout.write(
                        self.style.ERROR(
                            f"Ошибка загрузки логотипа {logo_url}: {str(e)} "
                            f"для {row['name']}"
                        )
                    )
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Ошибка: {str(e)}"))

        with open(
            os.path.join(base_path, "fundraisings.txt"), "r", encoding="utf-8"
        ) as f:
            reader = csv.DictReader(f, delimiter="\t")
            for row_num, row in enumerate(reader, 1):
                try:
                    status = (
                        FundraisingStatus.ACTIVE
                        if row["status"] == "Актуальный"
                        else FundraisingStatus.COMPLETED
                    )
                    existing_fundraising = TargetedFundraising.objects.filter(
                        title=row["title"]
                    ).first()
                    if not existing_fundraising and row.get("order"):
                        existing_by_order = TargetedFundraising.objects.filter(
                            order=row["order"]
                        ).first()
                        if existing_by_order:
                            existing_fundraising = existing_by_order
                    if existing_fundraising:
                        existing_fundraising.short_description = row[
                            "short_description"
                        ]
                        existing_fundraising.fundraising_link = row[
                            "fundraising_link"
                        ]
                        existing_fundraising.status = status
                        existing_fundraising.order = row["order"]
                        existing_fundraising.save()
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"Обновлен существующий адресный сбор (ID: "
                                f"{existing_fundraising.id}): {row['title']}"
                            )
                        )
                        fundraising = existing_fundraising
                    else:
                        fundraising = TargetedFundraising.objects.create(
                            title=row["title"],
                            short_description=row["short_description"],
                            fundraising_link=row["fundraising_link"],
                            status=status,
                            order=row["order"],
                        )
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"Создан новый адресный сбор (ID: "
                                f"{fundraising.id}): {row['title']}"
                            )
                        )
                    for i in range(1, 4):
                        photo_field = f"photo{i}"
                        if not row.get(photo_field):
                            continue
                        relative_path = row[photo_field].lstrip("\\/")
                        photo_url = f"{base_url}{relative_path}"
                        photo_filename = os.path.basename(relative_path)
                        photo_basename = os.path.splitext(
                            os.path.basename(relative_path)
                        )[0]
                        existing_photos = FundraisingPhoto.objects.filter(
                            fundraising=fundraising, position=i
                        )
                        existing_photo = None
                        for photo in existing_photos:
                            if photo.image and photo_basename in str(
                                photo.image
                            ):
                                existing_photo = photo
                                break
                        try:
                            if existing_photo:
                                existing_photo.title = (
                                    f"{photo_field}_{photo_basename}"
                                )
                                existing_photo.save()
                                self.stdout.write(
                                    self.style.SUCCESS(
                                        f"Обновлена существующая фотография "
                                        f"(ID: {existing_photo.id}) "
                                        f"для сбора (ID: {fundraising.id})"
                                    )
                                )
                            else:
                                response = requests.get(photo_url, timeout=10)
                                response.raise_for_status()

                                photo = FundraisingPhoto(
                                    title=f"{photo_field}_{photo_basename}",
                                    fundraising=fundraising,
                                    position=i,
                                )
                                photo.save()

                                photo.image.save(
                                    photo_filename,
                                    ContentFile(response.content),
                                    save=True,
                                )

                                self.stdout.write(
                                    self.style.SUCCESS(
                                        f"Загружена новая фотография (ID: "
                                        f"{photo.id}) для сбора (ID: "
                                        f"{fundraising.id}): {photo_url}"
                                    )
                                )
                        except requests.exceptions.RequestException as e:
                            self.stdout.write(
                                self.style.ERROR(
                                    f"Ошибка загрузки фотографии "
                                    f"{photo_url} для "
                                    f"{row['title']}: {str(e)}"
                                )
                            )
                        except Exception as e:
                            self.stdout.write(
                                self.style.ERROR(
                                    f"Ошибка при обработке фотографии: "
                                    f"{str(e)}"
                                )
                            )
                    for i in range(1, 4):
                        text_field = f"text{i}"
                        if not row.get(text_field):
                            continue
                        existing_text = FundraisingTextBlock.objects.filter(
                            fundraising=fundraising, position=i
                        ).first()
                        if existing_text:
                            existing_text.content = row[text_field]
                            existing_text.save()
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f"Обновлен текстовый блок (ID: "
                                    f"{existing_text.id}) "
                                    f"для сбора (ID: {fundraising.id})"
                                )
                            )
                        else:
                            text_block = FundraisingTextBlock.objects.create(
                                fundraising=fundraising,
                                position=i,
                                content=row[text_field],
                            )
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f"Создан новый текстовый блок (ID: "
                                    f"{text_block.id}) "
                                    f"для сбора (ID: {fundraising.id})"
                                )
                            )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(
                            f"Ошибка при обработке строки {row_num}: {str(e)}"
                        )
                    )

        self.stdout.write(self.style.SUCCESS("Данные успешно загружены!"))
