# custom_filters.py

from django import template
from django.utils.safestring import mark_safe
import re

register = template.Library()

@register.filter(name='censor')
def censor(value):
    unwanted_words = ['bad_word1', 'bad_word2', 'bad_word3']
    pattern = re.compile(r'\b(?:' + '|'.join(map(re.escape, unwanted_words)) + r')\b', re.IGNORECASE)
    censored_value = pattern.sub(lambda x: '*' * len(x.group(0)), value)
    return mark_safe(censored_value)
