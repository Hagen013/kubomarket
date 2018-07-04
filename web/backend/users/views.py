from django.views.generic import TemplateView

from cart.models import Order2


class ProfileView(TemplateView):
    """
    View для просмотра личной страницы пользователя
    """
    template_name = "pages/profile.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        user = self.request.user
        context["user"] = user
        context["orders"] = Order2.objects.filter(user=user)
        return context
