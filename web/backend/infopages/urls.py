from django.conf.urls import url, include
from django.views.generic import TemplateView


urls_infopages = [
    url(r'^oferta/$', TemplateView.as_view(template_name="pages/infopages/oferta.html"), name="oferta"),
    url(r'^policy/$', TemplateView.as_view(template_name="pages/infopages/policy.html"), name="policy"),
    url(r'^return/$', TemplateView.as_view(template_name="pages/infopages/return.html"), name="return"),
    url(r'^about/$', TemplateView.as_view(template_name="pages/infopages/about.html"), name="about"),
    url(r'^vacancies/$', TemplateView.as_view(
        template_name="pages/infopages/vacancies.html"), name="vacancies"),
    url(r'^cashback/$', TemplateView.as_view(
        template_name="pages/infopages/cashback.html"), name="cashback"),
    url(r'^agreement/$', TemplateView.as_view(
        template_name="pages/infopages/agreement.html"), name="agreement")
]
