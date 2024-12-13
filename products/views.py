from django.conf import settings
from django.db.models import Max, Min
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import View, DetailView
from products import VariableTypeText
from products.filters import ProductFilter
from products.models import Product, ProductVariant
from django.core.paginator import Paginator
from itertools import groupby
from django.db.models import Prefetch


class StoreView(View):
    template_name = "products/store.html"

    def get(self, request):
        filter_set = ProductFilter(request.GET, queryset=Product.objects.all().order_by('-id'))
        paginator = Paginator(filter_set.qs, 12)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context = {
            **ProductVariant.objects.aggregate(Max('price'), Min('price')),
            'products': filter_set,
            'page_obj': page_obj
        }
        if request.htmx:
            return render(request, template_name=f'{self.template_name}#product_list', context=context)
        return render(request, template_name=self.template_name, context=context)


class ProductDetailView(DetailView):
    template_name = "products/single-product.html"
    model = Product
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_variants = ProductVariant.objects.filter(product=self.object).prefetch_related(
            Prefetch('variant_image'),
            Prefetch('variables')
        ).distinct().order_by('variables__name')
        variants_queryset = product_variants.values(
            "variables__id", "variables__name", "variables__type"
        )
        gallery_images = [
            settings.MEDIA_URL + x["variant_image__image"]
            for x in product_variants.values("variant_image__image").distinct()
        ]
        variants = [
            {'type': key, 'text': VariableTypeText[key], 'items': list(group)}
            for key, group in groupby(variants_queryset, key=lambda x: x["variables__type"])
        ]
        print(variants)

        context['variants'] = variants
        context['gallery_images'] = gallery_images

        return context


def product_variants_choice(request, pk):
    variant_ids = [int(value.split('|')[1]) for value in request.POST.values()]
    product = get_object_or_404(Product, pk=pk)

    variants = product.variants.all()
    for variant_id in variant_ids:
        variants = variants.filter(variables=variant_id)

    if not variants.exists():
        return HttpResponse("موجود نیست")

    if len(variants) == 1:
        variant = variants.first()

        context = {
            "variant_id": variant.id,
            "stock": range(1, variant.stock + 1),
            "price": variant.get_price_text(),
            "discounted_price": variant.product.get_discounted_price(),
            "is_discounted": variant.product.is_discounted()
        }
        return render(request, "products/add-to-cart.html", context=context)

    response = HttpResponse()
    response.headers["HX-Reswap"] = "none"
    return response


def search_products(request):
    query = request.GET.get('q', '').strip()
    if query:
        products = Product.objects.filter(name__icontains=query)[:4]
    else:
        products = Product.objects.none()

    return render(request, template_name="products/search-result.html", context={'products': products})
