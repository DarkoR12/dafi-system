from django.contrib.auth import get_user_model
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.db import models
from django.urls import reverse

from meta.models import ModelMeta


class Club(ModelMeta, models.Model):
    '''
    Club
    '''

    name = models.CharField('nombre', max_length=64)

    slug = models.SlugField('slug', max_length=64)

    description = models.TextField('descripción', max_length=300)

    image = models.ImageField(
        'imagen', upload_to='clubs/', blank=True,
        help_text='Imagen para mostrar en la lista de clubes'
    )

    telegram_group = models.CharField(
        'grupo de telegram', max_length=64, blank=True, default=''
    )

    telegram_group_link = models.CharField(
        'enlace al grupo de telegram', max_length=64, blank=True, default=''
    )

    managers = models.ManyToManyField(
        get_user_model(), 'managed_clubs', verbose_name='gestores'
    )

    members = models.ManyToManyField(
        get_user_model(), 'clubs', verbose_name='miembros'
    )

    _metadata = {
        'title': 'name',
        'description': 'description',
        'image': 'get_image',
    }

    class Meta:
        verbose_name = 'club'
        verbose_name_plural = 'clubes'

        permissions = [
            ('can_link_club', 'Puede vincular un grupo de Telegram con un club')
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('clubs:detail', args=[self.slug])

    def get_image(self):
        return self.image.url if self.image else static('images/favicon.png')


class ClubMeeting(models.Model):
    '''
    Club meeting
    '''

    club = models.ForeignKey(
        Club, models.CASCADE, 'meetings', verbose_name='club'
    )

    title = models.CharField('título', max_length=200, blank=True)
    place = models.CharField('lugar', max_length=120)
    moment = models.DateTimeField('fecha')

    def __str__(self):
        return '{} en {} ({})'.format(
            self.club.name, self.place, self.moment.strftime('%d %b %Y %H:%M')
        )

    class Meta:
        verbose_name = 'quedada'

        ordering = ['moment']
