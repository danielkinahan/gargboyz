import django_tables2 as tables
from .models import Meme

class MemeTable(tables.Table):
    number = tables.Column(verbose_name='Number')
    declared_number = tables.Column(verbose_name='Declared number')
    meme_path = tables.TemplateColumn(template_name='meme_column.html', verbose_name='Meme')
    # meme_thumbnail
    # meme_type
    meme_created_at = tables.Column(verbose_name='Meme constructed')
    voice_recording_path = tables.TemplateColumn(template_name='recording_column.html', verbose_name='Idea')
    voice_recording_created_at = tables.Column(verbose_name='Idea date')
    voice_recording_transcript = tables.Column(verbose_name='Transcript')
    authors = tables.Column(verbose_name='Authors')
    season = tables.Column(verbose_name='Season')
    subseason = tables.Column(verbose_name='Subseason/Template')
    average_rating = tables.TemplateColumn(template_name='rating_column.html', verbose_name='Rating')
    actions = tables.TemplateColumn(template_name='actions_column.html', verbose_name='Actions')

    class Meta:
        model = Meme
        template_name = "django_tables2/bootstrap5-responsive.html"
        attrs = {"class": "table"}
        exclude = ['meme_type']
        sequence = ('number', 'meme_path', 'voice_recording_path', 'voice_recording_transcript',  
                    'authors', 'declared_number', 'voice_recording_created_at', 'season', 'meme_created_at', 'subseason')

        
    def render_authors(self, value):
        return ', '.join([author.name for author in value.all()])