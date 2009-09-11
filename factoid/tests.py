from django.template import Template, Context

from django.test import TestCase

class SimpleTest(TestCase):
    def test_contact_factoid(self):
        template = Template("""{% load factoids %}{% get_factoid 'greetings' as var %}""")
        # Check that nothing gets printed
        self.assertEqual(template.render(Context()), '')


    def test_printed_factoid(self):
        template = Template("""{% load factoids %}{% get_factoid 'greetings' %}""")
        # Basically just check that you got some string
        self.assertEqual(type(template.render(Context()))(), unicode())

