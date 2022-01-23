from django.dispatch import Signal


object_viewed_signal = Signal()

filter_signal = Signal()

search_signal = Signal()

"""object_viewed_signal = Signal(providing_args=['instance', 'request'])

filter_signal = Signal(providing_args=['queryset', 'request'])

search_signal = Signal(providing_args=['instance', 'request'])"""