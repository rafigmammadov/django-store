from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import ProductCategory, Product, Basket
from django.core.paginator import Paginator
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

class IndexView(TemplateView):
    template_name = 'products/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data()
        context['title'] = 'Rafistore'
        context['is_promote'] = True
        return context

class ProductListView(ListView):
    model = Product
    paginate_by = 3
    template_name = 'products/products.html'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data()
        context['title'] = 'Rafistore-Catalog'
        context['categories'] = ProductCategory.objects.all()
        return context

    def get_queryset(self):
        queryset = super(ProductListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category=category_id) if category_id else queryset



# def products(request, category_id=None, page=1):
#     products = Product.objects.filter(category=category_id) if category_id else Product.objects.all()
#     paginator = Paginator(products, 3)
#     products_paginator = paginator.page(page)
#
#     context = {
#         'title': 'Rafistore-Catalog',
#         'categories': ProductCategory.objects.all(),
#         'products': products_paginator,
#     }
#     return render(request, 'products/products.html', context)


@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])
