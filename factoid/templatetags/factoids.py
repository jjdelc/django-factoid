# -*- coding: utf-8 -*-

from django.template import Library, Node, TemplateSyntaxError

from factoid.models import Factoid

register = Library()

@register.simple_tag
def simple_get_factoid(type):
    """
    Returns a random factoid based on the type
    """
    try:
        factoid = Factoid.objects.get_random(type).body
    except Factoid.DoesNotExist:
        # In case an invalid type gets requested, return an empty string
        factoid = ''

    return factoid


@register.tag('get_factoid')
def do_get_factoid(parser, token):
    """
    Gets a random factoid, eithers prints it on context or stores it on a
    context variable

    {% get_factoid 'greetings' %}
    {% get_factoid 'greetings' as factoid %}

    """
    bits = token.split_contents()[::-1]
    tag_name = bits.pop() # Tag name is first bit

    if not bits:
        raise TemplateSyntaxError(u'%r requires at least one argument', tag_name)

    type = bits.pop() # Second argument is the type
    if type[0] in ('"', "'"): # Its a quoted param, lets remove them
        type = type[1:][:-1]

    if bits:
        as_var = bits.pop()
        if as_var != 'as':
            raise TemplateSyntaxError(u'Third argument mas be \'as\'')

        if not bits:
            raise TemplateSyntaxError(u'You have to specify a variable name')

        varname = bits.pop()
    else:
        varname = None

    return FactoidNode(type, varname)

class FactoidNode(Node):
    """
    Will either set a context variable wth the factoid or print it
    """

    def __init__(self, type, varname=None):
        self.varname = varname
        self.factoid = Factoid.objects.get_random(type).body

    def render(self, context):
        if self.varname is None:
            return self.factoid

        context[self.varname] = self.factoid
        return ''
