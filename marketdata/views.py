from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Currency, Product, ProductStatistics


class IndexView(generic.ListView):
    template_name = 'marketdata/index.html'
    context_object_name = 'productstats_list'

    def get_queryset(self):
        """Return most recent stats for each product."""
        products = Product.objects.all()
        most_recent_stats = []
        for product in products:
            ps = ProductStatistics.objects.filter(product=product).order_by('-last_updated')[0]
            most_recent_stats.append(ps)
        return most_recent_stats


class DetailView(generic.DetailView):
    model = Product
    template_name = 'marketdata/detail.html'


class CurrencyView(generic.DetailView):
    model = Currency
    template_name = 'marketdata/currency.html'
