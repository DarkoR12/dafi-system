from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.functional import cached_property

User = get_user_model()

NUM_YEARS = 4
YEARS_RANGE = range(1, NUM_YEARS + 1)
YEARS_VALIDATORS = [MinValueValidator(1), MaxValueValidator(NUM_YEARS)]


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
    year = models.IntegerField('año', validators=YEARS_VALIDATORS)

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


class Group(models.Model):
    '''Group of Students'''

    name = models.CharField(
        'nombre', max_length=64
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

    telegram_group = models.CharField(
        'grupo telegram', max_length=64, blank=True, default=''
    )

    telegram_channel = models.CharField(
        'canal telegram', max_length=64, blank=True, default=''
    )

    class Meta():
        verbose_name = 'grupo'

    def __str__(self):
        return self.name

    def subgroups_range(self):
        return range(1, self.subgroups + 1)


class Room(models.Model):
    name = models.CharField('nombre de la sala', max_length=64)
    code = models.CharField('código de la sala', max_length=64, unique=True)
    members = models.CharField('miembros en la sala', max_length=128, blank=True, default='')

    class Meta:
        verbose_name = 'sala'

    def __str__(self):
        return self.name

    def _get_members_list(self):
        try:
            return [int(x) for x in self.members.split(',')]
        except Exception:
            return []

    def _set_members_list(self, l):
        self.members = ','.join(str(x) for x in l)

    def get_members(self):
        return User.objects.filter(pk__in=self._get_members_list())

    def add_member(self, user):
        if not isinstance(user, User):
            raise TypeError('Must provide a valid user instance')

        l = self._get_members_list()

        if user.id in l:
            return

        l.append(user.id)

        self._set_members_list(l)
        self.save()

    def remove_member(self, user):
        if not isinstance(user, User):
            raise TypeError('Must provide a valid user instance')

        l = self._get_members_list()

        if user.id not in l:
            return

        l.remove(user.id)

        self._set_members_list(l)
        self.save()
