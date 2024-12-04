from django.views.generic import TemplateView
from ..Work_Views.service_application_view_mixin import ServiceApplicationViewMixin
from abc import ABC, abstractmethod


class BaseView(TemplateView, ServiceApplicationViewMixin, ABC):
    template_name = "applications/work-res/work-res-dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_specific_context())
        return context

    @abstractmethod
    def get_specific_context(self):
        """Sub-classes should implement this to provide view specific data"""
        pass


