from django import template

register = template.Library()

# FIXME Needs tests


@register.simple_tag(takes_context=True)
def query_string_with(context, **kwargs):
    dict_ = context.request.GET.copy()
    for k, v in kwargs.items():
        dict_[k] = v

    return "?" + dict_.urlencode()


@register.simple_tag(takes_context=True)
def query_string_without(context, *args):
    dict_ = context.request.GET.copy()

    for k in args:
        del dict_[k]

    return "?" + dict_.urlencode()
