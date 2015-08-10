from maps.models import StatementRequest
from maps.models import Statement
from maps.models import Article
from maps.models import Evidence
from maps.models import Figure
from maps.models import Measurement
from django.contrib import admin


admin.site.register( StatementRequest )
admin.site.register( Statement )
admin.site.register( Evidence )
admin.site.register( Article )
#admin.site.register( Figure )
#admin.site.register( Measurement )
