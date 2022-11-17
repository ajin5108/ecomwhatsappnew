from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import LoginRegister, UserRegistration
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from . models import MainBanner, SubBanners, Product, SubCategory, Category, Wishlist, Cart, Customer, AddToCart
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required


# Create your views here.
@csrf_exempt
def login_views(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pass')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if user.is_customer:
                return redirect('/')
        else:
            messages.info(request, 'Invalid Credentials')
    return render(request, 'web/login.html')

@csrf_exempt
def user_register(request):
    login_form = LoginRegister()
    user_form = UserRegistration()
    print("hi")
    if request.method == "POST":
        login_form = LoginRegister(request.POST)
        print(login_form)
        user_form = UserRegistration(request.POST)
        print(user_form)
        print("hlo")
        if login_form.is_valid() and user_form.is_valid():
            print("valid")
            user = login_form.save(commit=False)
            user.is_customer = True
            user.save()
            print("hloo")
            c = user_form.save(commit=False)
            c.user = user
            c.save()
            print("hloo")
            messages.info(request, 'User Registration Successfully')
            return redirect('user:login')
    return render(request, 'web/sign-up.html', {'login_form': login_form, 'user_form': user_form})



def index(request):
    mainbanner = MainBanner.objects.last()
    subbanners = SubBanners.objects.last()
    topsave = Product.objects.filter(is_top_save_today = True)
    bestseller = Product.objects.filter(is_best_seller = True).count()
    bestseller1 = Product.objects.filter(is_best_seller = True)[::-1]
    bestseller2 = Product.objects.filter(is_best_seller = True)[::-1]
    context = {
        "mainbanner":mainbanner,
        "subbanner":subbanners,
        "topsave":topsave,
        "bestseller1":bestseller1,
        "bestseller2":bestseller2
    }
    return render(request, "web/index.html", context)



def product(request, id):
    products = Product.objects.get(id=id)
    sub = products.subcategory
    context = {
        "products": products,
        "subcategory": sub
    }
    return render(request, "web/product-slider.html", context)



def shop(request,id):
    category = Category.objects.get(id=id)
    subcategory = SubCategory.objects.filter(id=id)
    context = {
        "category":category,
        "subcategory":subcategory
    }
    return render(request, "web/shop-left-sidebar.html", context)

# @csrf_protect
@login_required(login_url='login')
def addtowishlist(request,id):
        print("product0")
        if request.user.is_authenticated:
            print("product1")
            product = Product.objects.get(id=id)
            print("product3")
            if(product):
                print("product4")
                if(Wishlist.objects.filter(user=request.user.id,product=product)):
                     return JsonResponse({'status':"product is already in wishlist"})
                else:
                    my_p = Customer.objects.get(user=request.user)
                    print(my_p)
                    Wishlist.objects.create(user=my_p,product=product)
                   
                return JsonResponse({'status':"Product added successfully"}) 
            else:
                return JsonResponse({'status':"No such product found"})
        else:
            return JsonResponse({'status':"Login to Continue"})
        return redirect('/')


def viewwishlist(request):
    if request.user.is_authenticated:
        print("view0")
        my_p = Customer.objects.get(user=request.user)
        wished_item = Wishlist.objects.filter(user=my_p)
        print(wished_item)
        context= {
            'wished_items':wished_item
        }
        return render(request,'web/wishlist.html',context)  


@login_required(login_url='login')
def addtocart(request,id):
        if request.user.is_authenticated:
            print("product1")
            product = Product.objects.get(id=id)
            print("product3")
            if(product):
                print("product4")
                if(AddToCart.objects.filter(user=request.user.id,product=product)):
                    
                     return JsonResponse({'status':"product is already in cart"})
                else:  
                        my_p = Customer.objects.get(user=request.user)
                        print(my_p)
                        AddToCart.objects.create(user=my_p,product=product)
                        
                return JsonResponse({'status':"Product added successfully"}) 
            else:
                return JsonResponse({'status':"No such product found"})
        else:
            return JsonResponse({'status':"Login to Continue"})
        return redirect('/')
    
    
def viewcart(request):
    if request.user.is_authenticated:
        print("view0")
        my_p = Customer.objects.get(user=request.user)
        carted_item = Cart.objects.filter(user=my_p)
        print(carted_item)
        context= {
            'carted_item':carted_item
        }
        return render(request,'web/cart.html',context)    

    
# def viewcart(request):
#     print("cart0")
#     if request.user == None:
#         return redirect('user:login')
#         print("cart1")
#     else:
#         carted_item = Product.objects.get(id=id)
#         print("cart2")
#         Cart.save(carted_item)
#         print("cart3")
#     context = {
#         "carted_item" :carted_item
#     }
#     return render(request, "web/cart.html", context)    
    
    # if request.method == 'POST':
    #     print("cart0")
    #     if request.user.is_authenticated:
    #         p_id=int(request.POST.get('id'))
    #         product=Product.objects.get(product_id=p_id)
    #         if(product):
    #             if(Cart.objects.filter(user=request.user.id,product_id=p_id)):
    #                 return JsonResponse({'status':"product is already in cart"})
    #             else:
    #                 p_qty=int(request.POST.get('prod_quantity'))
    #                 if product.quantity >=p_qty:
    #                     Cart.objects.create(customer=request.user,product_id=p_id,product_qty=p_qty)
    #                     return JsonResponse({'status':"Product added successfully"})
    #                 else:
    #                     return JsonResponse({'status':"only "+str(product.quantity) + "quantity available"})
    #         else:
    #             return JsonResponse({'status':"No such product found"})
    #     else:
    #         return JsonResponse({'status':"Login to Continue"})
    # return redirect('/')





# def wishlist(request, id):
#     if request.user == None:
#         return redirect('user:login')
#     else:
#         request.user
#         wished_item = Product.objects.get(user=request.user)
#         Wishlist.save(wished_item)
#     context = {
#         "wished_item" :wished_item
#     }
#     return render(request, "web/wishlist.html", context)






def about_us(request):
    context = {}
    return render(request, "web/about-us.html", context)


def blog_detail(request):
    context = {}
    return render(request, "web/blog-detail.html", context)


def blog_grid(request):
    context = {}
    return render(request, "web/blog-grid.html", context)


def blog_list(request):
    context = {}
    return render(request, "web/blog-list.html", context)




def checkout(request):
    context = {}
    return render(request, "web/checkout.html", context)


def coming_soon(request):
    context = {}
    return render(request, "web/coming-soon.html", context)


def compare(request):
    context = {}
    return render(request, "web/compare.html", context)


def contact_us(request):
    context = {}
    return render(request, "web/contact-us.html", context)


def faq(request):
    context = {}
    return render(request, "web/faq.html", context)


def forgot(request):
    context = {}
    return render(request, "web/forgot.html", context)


def index_2(request):
    context = {}
    return render(request, "web/index-2.html", context)


def index_3(request):
    context = {}
    return render(request, "web/index-3.html", context)


def index_4(request):
    context = {}
    return render(request, "web/index-4.html", context)


def index_5(request):
    context = {}
    return render(request, "web/index-5.html", context)


def index_6(request):
    context = {}
    return render(request, "web/index-6.html", context)


def index_7(request):
    context = {}
    return render(request, "web/index-7.html", context)


def index_8(request):
    context = {}
    return render(request, "web/index-8.html", context)


def index_9(request):
    context = {}
    return render(request, "web/index-9.html", context)





def order_success(request):
    context = {}
    return render(request, "web/order-success.html", context)


def order_tracking(request):
    context = {}
    return render(request, "web/order-tracking.html", context)


def otp(request):
    context = {}
    return render(request, "web/otp.html", context)


def product_4_image(request):
    context = {}
    return render(request, "web/product-4-image.html", context)


def product_bottom_thumbnail(request):
    context = {}
    return render(request, "web/product-bottom-thumbnail.html", context)


def product_bundle(request):
    context = {}
    return render(request, "web/product-bundle.html", context)


def product_left_thumbnail(request):
    context = {}
    return render(request, "web/product-left-thumbnail.html", context)


def product_right_thumbnail(request):
    context = {}
    return render(request, "web/product-right-thumbnail.html", context)



def product_sticky(request):
    context = {}
    return render(request, "web/product-sticky.html", context)


def search(request):
    context = {}
    return render(request, "web/search.html", context)


def seller_become(request):
    context = {}
    return render(request, "web/seller-become.html", context)


def seller_dashboard(request):
    context = {}
    return render(request, "web/seller-dashboard.html", context)


def seller_detail_2(request):
    context = {}
    return render(request, "web/seller-detail-2.html", context)


def seller_detail(request):
    context = {}
    return render(request, "web/seller-detail.html", context)


def seller_grid_2(request):
    context = {}
    return render(request, "web/seller-grid-2.html", context)


def seller_grid(request):
    context = {}
    return render(request, "web/seller-grid.html", context)


def shop_banner(request):
    context = {}
    return render(request, "web/shop-banner.html", context)


def shop_category_slider(request):
    context = {}
    return render(request, "web/shop-category-slider.html", context)


def shop_category(request):
    context = {}
    return render(request, "web/shop-category.html", context)



def shop_list(request):
    context = {}
    return render(request, "web/shop-list.html", context)


def shop_right_sidebar(request):
    context = {}
    return render(request, "web/shop-right-sidebar.html", context)


def shop_top_filter(request):
    context = {}
    return render(request, "web/shop-top-filter.html", context)


def sign_up(request):
    context = {}
    return render(request, "web/sign-up.html", context)


def user_dashboard(request):
    context = {}
    return render(request, "web/user-dashboard.html", context)


def error_404(request):
    context = {}
    return render(request, "web/404.html", context)

