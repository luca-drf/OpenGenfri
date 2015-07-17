import datetime
from django import forms
from webpos.models import Category
from django.forms.extras.widgets import SelectDateWidget

# TIME_CHOICES = (
#         ('00', '00'),
#         ('01', '01'),
#         ('02', '02'),
#         ('03', '03'),
#     )


class ReportForm(forms.Form):
    # sel_category = forms.ModelChoiceField(queryset=Category.objects.all(),
    #                                       empty_label='All',
    #                                       required=False)
    date_start = forms.SplitDateTimeField(required=False)
    date_end = forms.SplitDateTimeField(required=False)
    # date_start = forms.DateField(widget=SelectDateWidget(), initial=datetime.date.today())
    # date_end = forms.DateField(widget=SelectDateWidget(), initial=datetime.date.today())
    # time_start = forms.ChoiceField(choices=TIME_CHOICES)
    # time_end = forms.ChoiceField(choices=TIME_CHOICES)

### DateTimeField formats
#
# ['%Y-%m-%d %H:%M:%S',    # '2006-10-25 14:30:59'
# '%Y-%m-%d %H:%M',        # '2006-10-25 14:30'
# '%Y-%m-%d',              # '2006-10-25'
# '%m/%d/%Y %H:%M:%S',     # '10/25/2006 14:30:59'
# '%m/%d/%Y %H:%M',        # '10/25/2006 14:30'
# '%m/%d/%Y',              # '10/25/2006'
# '%m/%d/%y %H:%M:%S',     # '10/25/06 14:30:59'
# '%m/%d/%y %H:%M',        # '10/25/06 14:30'
# '%m/%d/%y']              # '10/25/06'

class SearchForm(forms.Form):
    search = forms.CharField()
