# Generated by Django 2.0.2 on 2018-03-20 10:33

from django.db import migrations, models
import django.db.models.deletion
import django_react_templatetags.mixins


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0040_page_draft_title'),
        ('customimage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Base',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('og_title', models.CharField(blank=True, help_text='Fallbacks to seo title if empty', max_length=40, null=True, verbose_name='Facebook title')),
                ('og_description', models.CharField(blank=True, help_text='Fallbacks to seo description if empty', max_length=300, null=True, verbose_name='Facebook description')),
                ('twitter_title', models.CharField(blank=True, help_text='Fallbacks to facebook title if empty', max_length=40, null=True, verbose_name='Twitter title')),
                ('twitter_description', models.CharField(blank=True, help_text='Fallbacks to facebook description if empty', max_length=300, null=True, verbose_name='Twitter description')),
                ('robot_noindex', models.BooleanField(default=False, help_text='Check to add noindex to robots', verbose_name='No index')),
                ('robot_nofollow', models.BooleanField(default=False, help_text='Check to add nofollow to robots', verbose_name='No follow')),
                ('canonical_link', models.URLField(blank=True, null=True, verbose_name='Canonical link')),
                ('og_image', models.ForeignKey(blank=True, help_text='If you want to override the image used on Facebook for                     this item, upload an image here.                     The recommended image size for Facebook is 1200 × 630px', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='customimage.CustomImage')),
                ('twitter_image', models.ForeignKey(blank=True, help_text='Fallbacks to facebook image if empty', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='customimage.CustomImage', verbose_name='Twitter image')),
            ],
            options={
                'abstract': False,
            },
            bases=(django_react_templatetags.mixins.RepresentationMixin, 'wagtailcore.page'),
        ),
    ]
