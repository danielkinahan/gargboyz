import django_tables2 as tables
from .models import Meme

class MemeTable(tables.Table):
    large_hide_attr = {
        "td" : {'class': 'align-middle d-none d-lg-table-cell'},
        "th" : {'class': 'd-none d-lg-table-cell'}
    }
    medium_hide_attr = {
        "td" : {'class': 'align-middle d-none d-md-table-cell'},
        "th" : {'class': 'd-none d-md-table-cell'}
    }
    small_hide_attr = {
        "td" : {'class': 'align-middle d-none d-sm-table-cell'},
        "th" : {'class': 'd-none d-sm-table-cell'}
    }
    number = tables.TemplateColumn(template_name='memes/columns/number.html', verbose_name='Number', attrs=small_hide_attr)
    # declared_number = tables.Column(verbose_name='Declared number')
    meme_path = tables.TemplateColumn(template_name='memes/columns/meme.html', verbose_name='Meme', orderable=False)
    # meme_thumbnail
    # meme_type
    # meme_created_at = tables.Column(verbose_name='Meme constructed')
    voice_recording_path = tables.TemplateColumn(template_name='memes/columns/idea.html', verbose_name='Idea', orderable=False)
    voice_recording_created_at = tables.Column(verbose_name='Idea date', attrs=large_hide_attr)
    voice_recording_transcript = tables.Column(verbose_name='Transcript', orderable=False, attrs=large_hide_attr)
    authors = tables.Column(verbose_name='Authors', attrs=medium_hide_attr)
    season = tables.Column(verbose_name='Season', attrs=large_hide_attr)
    subseason = tables.Column(verbose_name='Subseason/Template', attrs=large_hide_attr)
    average_rating = tables.TemplateColumn(template_name='memes/columns/rating.html', verbose_name='Rating', attrs=small_hide_attr)
    comment_count = tables.TemplateColumn(template_name='memes/columns/actions.html', verbose_name='Actions', attrs=medium_hide_attr)

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