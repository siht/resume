from django.db import models

from wagtail.models import Page
from wagtail_resume.models import BaseResumePage


class HomePage(Page):
    pass


class ResumePage(BaseResumePage):
    pass
