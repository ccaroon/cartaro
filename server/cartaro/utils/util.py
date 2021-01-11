import sys
class Util:

    __DEFAULT_SORT_VALUE = {
        int: sys.maxsize * -1,
        str: '',
        bool: False
    }

    @classmethod
    # Used by the sort method.
    # Some model fields can be Null (None) and python
    # does not like to compare NoneType to int or str, etc.
    # This method attempts to find the field type by finding the first
    # non-None value and inspecting it.
    # Then we can look-up a valid default value to use in sorting.
    def __model_attr_type(cls, names, objs):
        types = []
        for attr in names:
            for obj in objs:
                if obj[attr] is not None:
                    types.append(type(obj[attr]))
                    break

        return types

    @classmethod
    def sort(cls, items, fields, reverse=False):
        types = cls.__model_attr_type(fields, items)
        def key_smith(o):
            return [cls.__DEFAULT_SORT_VALUE[types[i]] if o[f] == None else o[f] for i,f in enumerate(fields)]

        # In Place
        # items.sort(key=key_smith)
        # return None

        # As New List
        return sorted(items, key=key_smith, reverse=reverse)
