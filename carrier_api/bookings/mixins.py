from rest_framework.generics import get_object_or_404


class MultipleFieldLookupMixin(object):
    """
    Міксін для передавання декількох параметрів у посиланні
    За передачу полей відповідання змінна multiple_lookup_fields - тип кортеж
    Приклад:
    multiple_lookup_fields = ('ticket_no', 'flight_id')
    """
    def get_object(self):
        queryset = self.get_queryset()
        kw = {}
        for field in self.multiple_lookup_fields:
            kw[field] = self.kwargs[field]

        return get_object_or_404(queryset, **kw)
