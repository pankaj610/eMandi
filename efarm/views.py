from django.shortcuts import render
from django.http import *
from . import models
from . import forms
from django.urls import reverse
# Create your views here.

from cart.cart import Cart

def index(request):
    if not request.session.is_empty():
        if request.session['usr_type'] == "farmer":
            return HttpResponseRedirect(reverse('efarm:welcome_farmer'))
        elif request.session['usr_type'] == "customer":
            return HttpResponseRedirect(reverse('efarm:welcome_customer'))
    return render(request, "index.html")

def signup(request):
    if request.session.is_empty():
        return HttpResponseRedirect(reverse('efarm:login'))
    if request.method == "POST":
        signup_user = forms.SignupForm()
        if signup_user.is_valid():
            
            signup_user.save(commit=True)
            return HttpResponseRedirect(reverse("efarm:login"))
            # msg = "Enter Valid Details"
    # return HttpResponse("Hii")
    signup_form = forms.SignupForm()
    return render(request, "signup.html",{'signup_form':signup_form})

def login(request):
    msg=""
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = models.UserModel.objects.get(email = email,password =password)
            request.session['usr_key']=user.pk
            request.session['usr_type']=user.type
            if (user.type=="farmer"):
                return HttpResponseRedirect('welcome/farmer')
            elif (user.type == "customer"):
                return HttpResponseRedirect('welcome/customer')
        except models.UserModel.DoesNotExist:
            msg = "Enter Valid Details"
    return render(request, "login.html",{'msg':msg})

def logout(request):
    request.session.flush()
    return HttpResponseRedirect(reverse('efarm:login'))

from django.shortcuts import get_list_or_404, get_object_or_404
def welcomeFarmer(request, category_slug=None):
    if not request.session.is_empty():
        category=None
        categories = models.CropCategory.objects.all()
        crops = models.Crop.objects.all()
        if category_slug:
            category = get_object_or_404(models.CropCategory, slug=category_slug)
            crops = models.Crop.objects.filter(category=category)
        context = {
        'category': category,
        'categories': categories,
        'crops': crops
        }
        return render(request, "farmer/welcome.html", context)
    else:
        return HttpResponseRedirect(reverse('efarm:login'))

def welcomeCustomer(request, category_slug=None):
    if not request.session.is_empty():
        category=None
        categories = models.CropCategory.objects.all()
        crops = models.Crop.objects.all()
        if category_slug:
            category = get_object_or_404(models.CropCategory, slug=category_slug)
            crops = models.Crop.objects.filter(category=category)
        cart = Cart(request)
        context = {
        'category': category,
        'categories': categories,
        'crops': crops,
        'cart':cart
        }
        
        return render(request, "customer/welcome.html", context)
    else:
        return HttpResponseRedirect(reverse('efarm:login'))

def addCrop(request):
    if request.session.is_empty():
        return HttpResponseRedirect(reverse('efarm:login'))
    add_crop_form = forms.CropForm()
    if request.method =="POST":
        form = forms.CropForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print('-------------done-------------')
        else:
            print('-------------not done-------------')
    return render(request, "farmer/addCrop.html", {'add_crop':add_crop_form})

def cropDelete(request, object_id):
    if request.session.is_empty():
        return HttpResponseRedirect(reverse('efarm:login'))
    object = get_object_or_404(models.Crop, pk=object_id)
    object.delete()
    return HttpResponseRedirect(reverse("efarm:welcome_farmer"))



from django.views.generic import UpdateView
from .models import Crop
from .forms import CropForm
class EditCrop(UpdateView):
    model = Crop
    form_class = CropForm
    template_name = "farmer/editCrop.html"
    #
    # def get_object(self, *args, **kwargs):
    #     user = get_object_or_404(Crop, pk=self.kwargs['pk'])
    #
    #     # We can also get user object using self.request.user  but that doesnt work
    #     # for other models.
    #
    #     return user.userprofile

    def get_success_url(self, *args, **kwargs):
        # if request.session.is_empty():
        #     return HttpResponseRedirect(reverse('efarm:login'))
        return reverse("efarm:welcome_farmer")

def crop_list(request, category_slug=None):
    if request.session.is_empty():
        return HttpResponseRedirect(reverse('efarm:login'))
    category = None
    categories = models.CropCategory.objects.all()
    crops = models.Crop.objects.all()
    if category_slug:
        category = get_object_or_404(models.CropCategory, slug=category_slug)
        crops = models.Crop.objects.filter(category=category)

    context = {
        'category': category,
        'categories': categories,
        'crops': crops
    }
    if request.session['usr_type'] == "farmer":
        return render(request, 'farmer/welcome.html', context)
    elif request.session['usr_type'] == "customer":
        return render(request, 'customer/welcome.html', context)

from cart.forms import CartAddProductForm
# def verifyuser(request):
#     print(request.session['usr_type'])
def crop_detail(request, id, slug):
    if request.session.is_empty():
        # verifyuser(request)
        return HttpResponseRedirect(reverse('efarm:login'))
    crop = get_object_or_404(models.Crop, id=id, slug=slug)
    cart_product_form = CartAddProductForm()
    context = {
        'crop': crop,
        'cart_product_form': cart_product_form
    }
    return render(request,"customer/detail.html", context)


# -----------------------


def Home(request):
    if not request.session.is_empty():
        if request.session['usr_type'] == "farmer":
            return HttpResponseRedirect(reverse('efarm:welcome_farmer'))
        elif request.session['usr_type'] == "customer":
            return HttpResponseRedirect(reverse('efarm:welcome_customer'))
    return render(request,'index/e Mandi.html',{})


def Team(request):
    return render(request,'index/teams.html',{})


def Feed(request):
    if request.method == "POST":
        form = NameForm()
        print("-------------------------------------------")
        if form.is_valid():
            
            form.save(commit=True)
            a = feedback.objects.get(pk=1)
            f = NameForm(request.POST, instance=a)
            f.save()
            return HttpResponseRedirect(reverse('home'))
            # msg = "Enter Valid Details"
    # return HttpResponse("Hii")
    form = NameForm()
    if form.is_valid():
        form.save(commit=True)
    return render(request, "index/form.html",{'form':form})