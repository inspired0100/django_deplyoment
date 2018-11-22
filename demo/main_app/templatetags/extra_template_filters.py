from django import template

register = template.Library()

@register.filter(name='custom')
def replace(value,arg):
    return value.replace(arg, 'Checked')

    
