import django_tables2 as tables
from .models import Meme

class MemeTable(tables.Table):
    number = tables.TemplateColumn(template_name='memes/columns/number.html', verbose_name='Number')
    # declared_number = tables.Column(verbose_name='Declared number')
    meme_path = tables.TemplateColumn(template_name='memes/columns/meme.html', verbose_name='Meme', orderable=False)
    # meme_thumbnail
    # meme_type
    # meme_created_at = tables.Column(verbose_name='Meme constructed')
    voice_recording_path = tables.TemplateColumn(template_name='memes/columns/idea.html', verbose_name='Idea', orderable=False)
    voice_recording_created_at = tables.Column(verbose_name='Idea date')
    voice_recording_transcript = tables.Column(verbose_name='Transcript', orderable=False)
    authors = tables.Column(verbose_name='Authors')
    season = tables.Column(verbose_name='Season')
    subseason = tables.Column(verbose_name='Subseason/Template')
    average_rating = tables.TemplateColumn(template_name='memes/columns/rating.html', verbose_name='Rating')
    comment_count = tables.TemplateColumn(template_name='memes/columns/actions.html', verbose_name='Actions')

    class Meta:
        model = Meme
        template_name = "django_tables2/bootstrap5-responsive.html"
        attrs = {
           'td': {'class': 'align-middle'}
        }
        exclude = ['meme_type', 'rating_count',  'declared_number', 'meme_created_at']
        sequence = ('comment_count', 'average_rating', 'number', 'meme_path', 'voice_recording_path', 'voice_recording_transcript',  
                    'authors', 'voice_recording_created_at', 'season', 'subseason')

        
    def render_authors(self, value):
        return ', '.join([author.name for author in value.all()])