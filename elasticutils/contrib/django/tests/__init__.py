# We need to put these in a separate module so they're easy to import
# on a test-by-test basis so that we can skip django-requiring tests
# if django isn't installed.


from elasticutils.contrib.django import MappingType, Indexable


_model_cache = []


def reset_model_cache():
    del _model_cache[0:]


class Meta(object):
    def __init__(self, db_table):
        self.db_table = db_table


class Manager(object):
    def filter(self, id__in=None):
        return [m for m in _model_cache if m.id in id__in]


class FakeModel(object):
    _meta = Meta('fake')
    objects = Manager()

    def __init__(self, **kw):
        self._doc = kw
        for key in kw:
            setattr(self, key, kw[key])
        _model_cache.append(self)


class FakeDjangoMappingType(MappingType, Indexable):
    @classmethod
    def get_model(cls):
        return FakeModel

    @classmethod
    def extract_document(cls, obj_id, obj=None):
        if obj is None:
            raise ValueError('I\'m a dumb mock object and I have no idea '
                             'what to do with these args.')

        return obj._doc
