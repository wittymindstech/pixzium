import os

from django.core.management.base import BaseCommand
import random
import datetime
from wtgallery.models import Profile, Image
from django.contrib.auth.models import User
from lorem_text import lorem as lt
from django.core.files import File

TAGS = [
    'Sports', 'Lifestyle', 'Music',
    'Coding', 'Travelling', 'coder',
    'river', 'bones', 'whale',
    'Fishes', 'Anaconda', 'human',
    'avangers', 'waterfall', 'Book',
    'ocean', 'sea', 'Superman',
]

Usernames = [
    'john', 'michael', 'luke', 'sally', 'joe', 'james',
]

Lastnames = [
    'McAolleny', 'andrew', 'el', 'junior', 'stark', 'widow',
]


def generate_description():
    return lt.words(random.randint(50, 80))


def generate_user_name():
    index = random.randint(0, 5)
    return Usernames[index]


def generate_profile_heading():
    return lt.words(random.randint(5, 9))


def generate_title_name():
    word_count = random.randint(4, 8)
    return lt.words(word_count)


def generate_tags_name():
    index = random.randint(0, 9)
    return TAGS[index]


def generate_is_freelance():
    value = random.randint(0, 1)
    if value == 0:
        return False
    return True


def generate_is_verified():
    value = random.randint(0, 1)
    if value == 0:
        return False
    return True


def generate_upload_date():
    year = random.randint(2019, 2021)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return datetime.date(year, month, day)


def generate_profile():
    username = generate_user_name()
    user = User.objects.get_or_create(username=username)
    if user[1]:
        user[0].set_password('Ab@123#123')
        user[0].first_name = username
        user[0].last_name = Lastnames[random.randint(0, 5)]
        user[0].save()
    profile_heading = generate_profile_heading()
    description = generate_description()
    freelance = generate_is_freelance()
    verified = generate_is_verified()
    profile = Profile.objects.get_or_create(user=user[0])
    if profile[1]:
        profile[0].profileheading = profile_heading,
        profile[0].description = description,
        profile[0].freelance = freelance
        profile[0].verified = verified
        profile[0].save()
    return profile[0]


def generate_image_status():
    choices = ['A', 'P']
    return choices[random.randint(0, 1)]


def get_path_to_image(image_path):
    list_of_image_names = os.listdir(image_path)
    return list_of_image_names
    # index = random.randint(0, len(list_of_image_names)-1)
    # return list_of_image_names[index], os.path.abspath(f"sample/{list_of_image_names[index]}")


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('file_name', type=str, help="The text file that contains the image titles")
        parser.add_argument('path_to_images', type=str, help="The directory that contains the sample images")

    def handle(self, *args, **kwargs):
        file_name = kwargs['file_name']
        path_to_images = kwargs['path_to_images']
        list_image_names = get_path_to_image(path_to_images)
        counts = 0
        for image_file in list_image_names:
            image = Image()
            image.user = generate_profile()
            image.title = generate_title_name()
            image.description = generate_description()
            image.uploaded_at = generate_upload_date()
            image.status = generate_image_status()
            path_to_file = os.path.abspath(f"sample/{image_file}")
            image.file.save(image_file, File(open(path_to_file, 'rb')))
            image.save()
            for _ in range(0, random.randint(1, 6)):
                image.tags.add(generate_tags_name())
            image.save()
            counts += 1
        self.stdout.write(self.style.SUCCESS(f'Data Imported Successfully\n Total of {counts} images imported and 6 User profiles created\n default password: "Ab@123#123"\n'))
