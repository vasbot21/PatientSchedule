from django.contrib import admin
from .models import *


class ExamAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ['name']


class SpecialistAdmin(admin.ModelAdmin):
    list_display = ('surname', 'name', 'patronymic', 'position')
    filter_horizontal = ['exam_list']


class PatientAdmin(admin.ModelAdmin):
    list_display = ('surname', 'name', 'patronymic', 'phone', 'birth_year', 'black_list')
    search_fields = ['surname', 'name', 'patronymic', 'phone', 'birth_year', 'black_list']
    actions = ['add_to_black_list', 'delete_from_black_list']

    @admin.action(description='Добавить в черный список')
    def add_to_black_list(self, request, queryset):
        queryset.update(black_list=True)

    @admin.action(description='Убрать из черного списка')
    def delete_from_black_list(self, request, queryset):
        queryset.update(black_list=False)


class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('patient', 'time_start', 'time_end', 'come')
    list_filter = ['time_start', 'time_end', 'come']
    filter_horizontal = ['exam_list']


class SpecialistCalendarAdmin(admin.ModelAdmin):
    list_display = ['date']
    list_filter = ['date']
    search_fields = ['date']
    filter_horizontal = ['specialists']


admin.site.register(Exam, ExamAdmin)
admin.site.register(Specialist, SpecialistAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Registration, RegistrationAdmin)
admin.site.register(SpecialistCalendar, SpecialistCalendarAdmin)
