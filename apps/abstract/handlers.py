from typing import (
    Optional,
)
from urllib import response
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse

from abstract.mixins import HttpResponseMixin


class ViewHandler(HttpResponseMixin):
    """Handler for validating request and generating response."""

    template_login_page: str = 'app1/login.html'

    def get_validated_response(
        self,
        request: WSGIRequest
    ) -> Optional[HttpResponse]:
        """Get validated response."""

        if request.user.is_authenticated:
            return None

        return self.get_http_response(
            request,
            self.template_login_page
        )
        response:Optional[HttpResponse] = \
            self.get_validated_response(
                request
            )
        if response:
            return response