from .signals import object_viewed_signal, filter_signal, search_signal

class ObjectViewMixin(object):
    def dispatch(self, request, *args,**kwargs):
        try:
            instance = self.get_object()
        except DoesNotExist:
            instance = None
        if instance is not None:
            object_viewed_signal.send(instance.__class__, instance=instance, request=request)
        return super(ObjectViewMixin, self).dispatch(request, *args, **kwargs)

class FilterViewMixin:
    def dispatch(self, request, *args,**kwargs):
        page="FilterPage"
        try:
            queryset = self.get_queryset()
        except DoesNotExist:
            queryset = None
        if queryset is not None:
            filter_signal.send(page, queryset=queryset, request=request)
        return super(FilterViewMixin, self).dispatch(request, *args, **kwargs)     

class SearchViewMixin:
    def dispatch(self, request, *args,**kwargs):
        page="SearchPage"
        try:
            queryset = self.get_queryset()
        except DoesNotExist:
            queryset = None
        if queryset is not None:
            search_signal.send(page, queryset=queryset, request=request)
        return super(SearchViewMixin, self).dispatch(request, *args, **kwargs)     