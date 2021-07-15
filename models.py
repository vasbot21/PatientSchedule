from django.db import models
import locale

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')


class Patient(models.Model):
    surname = models.CharField(max_length=50, verbose_name='Фамилия')
    name = models.CharField(max_length=50, verbose_name='Имя')
    patronymic = models.CharField(max_length=50, verbose_name='Отчество', null=True, blank=True)
    phone = models.CharField(max_length=10, verbose_name='Телефон')
    birth_year = models.CharField(max_length=4, verbose_name='Год рождения', null=True, blank=True)
    black_list = models.BooleanField(default=False, verbose_name='Черный список')
    text = models.TextField(null=True, blank=True, verbose_name='Примечание')

    def format_phone(self):
        return '+7 (' + self.phone[:3] + ')-' + self.phone[3:6] + '-' + self.phone[6:8] + '-' + self.phone[8:10]

    def __str__(self):
        res = self.surname + ' ' + self.name
        if self.patronymic:
            res += ' ' + self.patronymic
        res += ' Тел.: ' + self.phone
        if self.birth_year:
            res += ' Год рождения: ' + self.birth_year
        return res

    class Meta:
        verbose_name = 'Пациент'
        verbose_name_plural = 'Пациенты'


class Exam(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название исследования')
    price = models.PositiveSmallIntegerField(verbose_name='Цена')

    def __str__(self):
        return self.name + ': ' + str(self.price) + ' тг'

    class Meta:
        verbose_name = 'Исследование'
        verbose_name_plural = 'Исследования'


class Specialist(models.Model):
    surname = models.CharField(max_length=50, verbose_name='Фамилия')
    name = models.CharField(max_length=50, verbose_name='Имя')
    patronymic = models.CharField(max_length=50, verbose_name='Отчество')
    position = models.CharField(max_length=200, verbose_name='Должность')
    exam_list = models.ManyToManyField(Exam, verbose_name='Список исследований')

    def __str__(self):
        if self.patronymic:
            return self.surname + ' ' + self.name + ' ' + self.patronymic + ' - ' + self.position
        else:
            return self.surname + ' ' + self.name + ' - ' + self.position

    class Meta:
        verbose_name = 'Врач'
        verbose_name_plural = 'Врачи'


class Registration(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name='Пациент')
    time_start = models.DateTimeField('Начало приема')
    time_end = models.DateTimeField('Конец приема')
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE, verbose_name='Врач')
    exam_list = models.ManyToManyField(Exam, verbose_name='Список исследований')
    who_sent = models.CharField(max_length=200, null=True, blank=True, verbose_name='Кто направил')
    text = models.TextField(null=True, blank=True, verbose_name='Примечание')
    come = models.BooleanField(default=False, verbose_name='Пришел')

    def __str__(self):
        return self.patient.__str__() + ' Когда:' + self.time_start.strftime("%d %B %Y") + ' ' + \
               self.time_start.strftime("%H:%M") + '-' + self.time_end.strftime("%H:%M") + ' Примечание: ' + self.text

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'


class SpecialistCalendar(models.Model):
    date = models.DateField('Рабочий день')
    specialists = models.ManyToManyField(Specialist, verbose_name='Врачи')

    def __str__(self):
        return self.date.strftime("%d %B %Y")

    class Meta:
        verbose_name = 'Рабочий день'
        verbose_name_plural = 'Рабочие дни'
