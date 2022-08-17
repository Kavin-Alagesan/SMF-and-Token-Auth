from django.contrib import admin
from .models import ProgressModel,StudentDetailModel

# Register your models here.
admin.site.register(StudentDetailModel)
admin.site.register(ProgressModel)

