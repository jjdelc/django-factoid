# -*- coding: utf-8 -*-

from random import choice

from django.db import models
from django.core.cache import cache

class FactoidType(models.Model):
    FACTS_IDS = 'factoid:type_ids:%s'

    name = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name.title()

    def save(self, *args, **kwargs):
        # Make sure all names are stored in lowercase
        self.name = self.name.lower()
        super(FactoidType, self).save(*args, **kwargs)

class FactoidManager(models.Manager):
    def get_random(self, type):
        """
        Fetch a random Factoid based on the requested type
        Store the available id list in cache per type
        """
        type = type.lower()
        fact_ids = cache.get(FactoidType.FACTS_IDS % type)

        if fact_ids is None:
            try:
                factoid_type = FactoidType.objects.get(name=type)
            except FactoidType.DoesNotExist:
                return Factoid(body='')

            fact_ids = super(FactoidManager, self).get_query_set().filter(
                type=factoid_type).values_list('id', flat=True)
            cache.set(FactoidType.FACTS_IDS % type, fact_ids)

        # This one HAS to exist right?
        factoid = super(FactoidManager, self).get(pk=choice(fact_ids))

        return factoid
            


class Factoid(models.Model):
    type = models.ForeignKey(FactoidType)
    body = models.TextField()

    objects = FactoidManager()

    def __unicode__(self):
        return u'[%s] %s ...' % (self.type, self.body[:15])

    def save(self, *args, **kwargs):
        """
        Clean the cache when a factoid has been modified or created
        """
        cache.delete(FactoidType.FACTS_IDS % self.type.id)
        super(Factoid, self).save(*args, **kwargs)

