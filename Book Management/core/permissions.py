from django.http import HttpResponseForbidden


def book_delete_permission(function):
    def wrapper(request, *args, **kwargs):
        if request.user.has_perm('core.delete_book'):
            return function(request, *args, **kwargs)
        else:
            return HttpResponseForbidden('You do not have permission to perform this action.')

    return wrapper


def book_update_permission(function):
    def wrapper(request, *args, **kwargs):
        if request.user.has_perm('core.update_book'):
            return function(request, *args, **kwargs)
        else:
            return HttpResponseForbidden('You do not have permission to perform this action.')

    return wrapper


def book_add_permission(function):
    def wrapper(request, *args, **kwargs):
        if request.user.has_perm('core.add_book'):
            return function(request, *args, **kwargs)
        else:
            return HttpResponseForbidden('You do not have permission to perform this action.')

    return wrapper
