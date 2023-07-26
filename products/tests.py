from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from products.models import Product, ProductCategory


class IndexTestView(TestCase):

    def test_view(self):
        path = reverse('index')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context['title'], 'Rafistore')
        self.assertTemplateUsed(response, 'products/index.html')


class ProductListTestView(TestCase):
    fixtures = ['categories.json', 'goods.json']

    def setUp(self):
        self.products = Product.objects.all()
        self.category = ProductCategory.objects.first()

    def test_products_list_view(self):
        path = reverse('products:index')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context['title'], 'Rafistore-Catalog')
        self.assertTemplateUsed(response, 'products/products.html')
        self.assertEqual(list(response.context_data['object_list']), list(self.products[:3]))

    def test_products_category(self):
        path = reverse('products:category', kwargs={'category_id': self.category.id})
        response = self.client.get(path)


        self.assertEqual(list(response.context_data['object_list']), list(self.products.filter(category_id=self.category.id)))
