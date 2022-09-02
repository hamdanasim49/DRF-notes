from notes.models.models import Notes
from django_filters import FilterSet, BooleanFilter


class NotesArchiveFilter(FilterSet):
    archive = BooleanFilter(method="filter_is_archive")
    print("In file filter***")

    class Meta:
        model = Notes
        fields = [
            "archive",
        ]

    def filter_is_archive(self, queryset, name, value):
        print("Bro")
        if value:
            print("Allo", value)
            return queryset.filter(archive=True)
        else:
            return queryset.filter(archive=False)
