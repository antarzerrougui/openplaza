from itertools import chain
from django.forms import widgets,ModelForm,ModelChoiceField
from django.utils.encoding import StrAndUnicode, force_unicode
from django.utils.html import escape, conditional_escape
from .models import Category,Product

class NodeWidget(widgets.Select):
    def render(self, name, value, attrs=None, choices=()):
        return []

    def render_options(self, choices, selected_choices):
        selected_choices = set(force_unicode(v) for v in selected_choices)
        output = []
        for option_value, option_label in chain(self.choices, choices):
            if isinstance(option_label, (list, tuple)):
                output.append(u'<optgroup label="%s">' % escape(force_unicode(option_value)))
                for option in option_label:
                    output.append(self.render_option(selected_choices, *option))
                output.append(u'</optgroup>')
            else:
                output.append(self.render_option(selected_choices, option_value, option_label))
        return u'\n'.join(output)


class CategoryModelForm(ModelForm):
    #parent_node_id = ModelChoiceField(widget = NodeWidget)
    exclude = ('parent_id',)
    class meta:
        model = Category
        widgets = {
            "parent_id" : widgets.TextInput
        }

class ProductModelForm(ModelForm):
    class meta:
        model = Product