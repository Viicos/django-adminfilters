from django import forms
from django.contrib.admin import FieldListFilter, ListFilter, SimpleListFilter
from django.contrib.admin.options import ModelAdmin


class WrappperMixin:
    negated = False
    can_negate = False
    title = None
    negated_title = None

    def __init__(self, *args, **kwargs) -> None:
        self.error = None
        self.error_message = None
        super().__init__(*args, **kwargs)

    def html_attrs(self):
        classes = f'adminfilters box {self.__class__.__name__.lower()}'
        if self.error_message:
            classes += ' error'

        return {'class': classes,
                'id': '_'.join(self.expected_parameters()),
                }

    def get_title(self):
        if not self.can_negate and self.negated:
            if self.negated_title:
                return self.negated_title
            else:
                return f'not {self.title}'
        return self.title


class SmartListFilter(WrappperMixin, ListFilter):
    pass


class SmartSimpleListFilter(WrappperMixin, SimpleListFilter):
    pass


class SmartFieldListFilter(WrappperMixin, FieldListFilter):
    pass


class MediaDefinitionFilter:
    def __init__(self, *args, **kwargs):
        model_admin = kwargs.get('model_admin', None)
        if model_admin and not isinstance(model_admin, AdminFiltersMixin):
            raise Exception(
                f'{self.__class__.__name__} needs that the {model_admin.__class__.__name__} '
                f'that use it extends AdminFiltersMixin')
        super().__init__(*args, **kwargs)


class AdminFiltersMixin(ModelAdmin):

    def get_changelist_instance(self, request):
        cl = super().get_changelist_instance(request)
        for flt in cl.filter_specs:
            if hasattr(flt, 'media'):
                self.admin_filters_media += flt.media
        return cl

    def __init__(self, model, admin_site):
        self.admin_filters_media = forms.Media()
        super().__init__(model, admin_site)

    @property
    def media(self):
        original = super().media
        if hasattr(self, 'admin_filters_media'):
            original += self.admin_filters_media
        return original