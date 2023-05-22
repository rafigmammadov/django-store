from django.shortcuts import render


def index(request):
    context = {
        'title': 'Rafistore',
        'is_promote': True,
    }
    return render(request, 'products/index.html', context)


def products(request):
    context = {
        'title': 'Rafistore-Catalog',
        'products': [
            {
                'name': 'adidas Originals Black Monogram Hoodie',
                'price': '75',
                'image': '/static/vendor/img/products/Adidas-hoodie.png',
                'description': 'Soft fabric for sweatshirts. Style and comfort is a way of life.'
            },

            {
                'name': 'The North Face blue jacket',
                'price': '295',
                'image': '/static/vendor/img/products/Blue-jacket-The-North-Face.png',
                'description': 'Smooth fabric. Waterproof coating. Light and warm',
            },

            {
                'name': 'ASOS DESIGN oversized sports top in brown',
                'price': '42',
                'image': '/static/vendor/img/products/Brown-sports-oversized-top-ASOS-DESIGN.png',
                'description': 'Plush material. Comfortable and soft.',
            },

            {
                'name': 'Nike Black Heritage Backpack',
                'price': '30',
                'image': '/static/vendor/img/products/Black-Nike-Heritage-backpack.png',
                'description': 'Thick fabric. Lightweight material',
            },

            {
                'name': 'Dr Martens 1461 Bex Black 3-Eye Platform Shoes',
                'price': '170',
                'image': '/static/vendor/img/products/Black-Dr-Martens-shoes.png',
                'description': 'Dr Martens black 3-eye platform shoes',
            },

            {
                'name': 'ASOS DESIGN wide leg tailored trousers in navy',
                'price': '35',
                'image': '/static/vendor/img/products/Dark-blue-wide-leg-ASOs-DESIGN-trousers.png',
                'description': 'Lightweight stretch seersucker fabric Textured fabric',
            }
        ]
    }
    return render(request, 'products/products.html', context)
