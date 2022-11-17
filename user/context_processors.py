from user.models import Category
from user.models import SubCategory
from user.models import Product
from user.models import HeaderFlash


def main_context(request):
    headerflash = HeaderFlash.objects.last()
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    products = Product.objects.all()
    return {"headerflash": headerflash, "categories": categories, "subcategories": subcategories, "products": products}
