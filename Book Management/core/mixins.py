from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseForbidden


class AddBookMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.has_perm('core.add_book'):
            return super().dispatch(request, *args, **kwargs)

        return HttpResponseForbidden('You Do not have permission to access this page.')


class UpdateBookMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.has_perm('core.change_book'):
            return super().dispatch(request, *args, **kwargs)

        return HttpResponseForbidden('You Do not have permission to access this page.')


class DeleteBookMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.has_perm('core.delete_book'):
            return super().dispatch(request, *args, **kwargs)

        return HttpResponseForbidden('You Do not have permission to access this page.')
