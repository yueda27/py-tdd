from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ValidationError

from lists.models import Item, List

# Create your views here.
def home_page(request):
    return render(request, 'home.html') 

def view_list(request, list_id):
    list_ = List.objects.get(id = list_id)
    items = Item.objects.filter(list = list_)
    return render(request, 'list.html',{'list': list_,} ) 

def new_list(request):
    list_ = List.objects.create()
    item = Item.objects.create(text=request.POST.get('item_text', ''), list = list_)
    try:
        item.full_clean()
    except ValidationError:
        list_.delete()
        return render(request,"home.html", {'error': "You can't have an empty list"})

    return redirect(f'/lists/{list_.id}/')

def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST.get('item_text', ''), list = list_)
    return redirect(f'/lists/{list_.id}/')