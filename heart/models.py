from os.path import basename

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.functional import cached_property

User = get_user_model()

NUM_YEARS = 4
YEARS_RANGE = range(1, NUM_YEARS + 1)
YEARS_VALIDATORS = [MinValueValidator(1), MaxValueValidator(NUM_YEARS)]


class Group(models.Model):
    '''Group of Students'''

    name = models.CharField(
        'nombre', max_length=64
    )

    number = models.IntegerField(
        'número de grupo', blank=True, null=True
    )

    year = models.IntegerField(
        'año', validators=YEARS_VALIDATORS
    )

    subgroups = models.IntegerField(
        'número de subgrupos', validators=[
            MinValueValidator(1), MaxValueValidator(4)
        ]
    )

    delegate = models.ForeignKey(
        User, models.PROTECT, blank=True, null=True, related_name='delegate_group',
        verbose_name='delegado'
    )

    subdelegate = models.ForeignKey(
        User, models.PROTECT, blank=True, null=True, related_name='subdelegate_group',
        verbose_name='subdelegado'
    )

    telegram_group = models.CharField(
        'grupo de telegram', max_length=64, blank=True, default=''
    )

    telegram_group_link = models.CharField(
        'enlace al grupo de telegram', max_length=64, blank=True, default=''
    )

    class Meta():
        verbose_name = 'grupo'

        permissions = [
            ('can_link_group', 'Puede vincular un grupo de Telegram con un grupo de alumnos')
        ]

    def __str__(self):
        return 'Año {} {}'.format(self.year, self.name)

    def subgroups_range(self):
        return range(1, self.subgroups + 1)


class Year(models.Model):
    '''
    Academic Year
    '''

    id = models.IntegerField('año', primary_key=True, validators=[MinValueValidator(1), MaxValueValidator(4)])
    groups = models.IntegerField('número de grupos', validators=[MinValueValidator(1), MaxValueValidator(4)])
    subgroups = models.IntegerField('número de subgrupos', validators=[MinValueValidator(1), MaxValueValidator(3)])

    class Meta:
        verbose_name = 'año'

    def __str__(self):
        return 'Año {}'.format(self.id)

    @cached_property
    def i(self):
        return self.id - 1

    def groups_range(self):
        return range(1, self.groups + 1)

    def subgroups_range(self):
        return range(1, self.subgroups + 1)


class Subject(models.Model):
    '''
    Academic subject
    '''

    QUARTERS = [
        (1, 'Primer cuatrimestre'),
        (2, 'Segundo cuatrimestre'),
    ]

    code = models.IntegerField('código', primary_key=True)
    name = models.CharField('nombre', max_length=64)
    acronym = models.CharField('siglas', max_length=6)
    quarter = models.IntegerField('cuatrimestre', choices=QUARTERS, default=1)
    year = models.ForeignKey(Year, models.PROTECT, related_name='subjects', verbose_name='año')

    class Meta:
        verbose_name = 'asignatura'

    def __str__(self):
        return '{} {} ({})'.format(self.code, self.name, self.acronym)

    @classmethod
    def get_grouped(cls):
        d = cache.get('grouped_subjects')

        if not d:
            d = {}

            for s in cls.objects.all():
                if s.year not in d:
                    d[s.year] = []

                d[s.year].append(s)

            cache.set('grouped_subjects', d)

        return d


class DocumentMedia(models.Model):
    '''Document and media files'''

    name = models.CharField('nombre', max_length=120)

    file = models.FileField('archivo', upload_to='docs/')

    hidden = models.BooleanField(
        'oculto', default=False,
        help_text='Ocultar el archivo en las listas'
    )

    class Meta:
        verbose_name = 'documento'

    def __str__(self):
        return self.name

    def get_filename(self):
        return basename(self.file.name)
