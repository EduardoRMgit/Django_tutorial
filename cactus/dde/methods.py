from itertools import chain


def to_dict(instance):
    opts = instance._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields):
        if f.name == 'user':
            continue
        value = f.value_from_object(instance)
        if value is None:
            continue
        data[f.name] = str(value)
    for f in opts.many_to_many:
        data[f.name] = [i.id for i in f.value_from_object(instance)]
    return data
