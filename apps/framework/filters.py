from django_filters import Filter
from django_filters.fields import Lookup
from django_filters.filters import DateFilter
from datetime import date, datetime, time


class ListFilter(Filter):

    def filter(self, qs, value):
        value_list = value.split(u',')
        if len(value_list) > 0 and value_list[0]:
            return super(ListFilter, self).filter(qs, Lookup(value_list, 'in'))
        return qs


class WithinDateFilter(DateFilter):

    def filter(self, qs, value):
        from datetime import timedelta

        if value:

            value = datetime.combine(value, time.min)

            filter_lookups = {
                "%s__range" % (self.name, ): (
                    value,
                    value + timedelta(days=1),
                ),
            }

            qs = qs.filter(**filter_lookups)

        return qs


class AfterDateFilter(DateFilter):

    def filter(self, qs, value):

        if value:

            date_value = datetime.combine(value, time.min)

            filter_lookups = {
                "%s__gt" % (self.name, ): (
                    date_value
                ),
            }

            qs = qs.filter(**filter_lookups)

        return qs


class BeforeDateFilter(DateFilter):

    def filter(self, qs, value):

        if value:

            date_value = datetime.combine(value, time.min)

            filter_lookups = {
                "%s__lt" % (self.name, ): (
                    date_value
                ),
            }

            qs = qs.filter(**filter_lookups)

        return qs
