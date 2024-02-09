from django.shortcuts import redirect, render
from django.urls import reverse
from rango.models import Page, Category
from django.http import HttpResponse
from rango.forms import CategoryForm, PageForm

def show_category(request, category_name_slug):
    # Create a context dictionary which we can pass to the template rendering engine.
    # to the template rendering engine.
    context_dict = {}
    
    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # The .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug)
        
        # Retrieve all of the associated pages.
        # Note that filter() will return a list of page objects or an empty list.
        pages = Page.objects.filter(category=category)
        
        # Adds our results list to the template context under name pages.
        context_dict['pages'] = pages
        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['category'] = category
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        context_dict['category'] = None
        context_dict['pages'] = None
        
    # Go render the response and return it to the client.
    return render(request, 'rango/category.html', context=context_dict)
    


def index(request):
    # Query the database for a list of ALL categories currently stored.
    # Order the categories by no. likes in descending order.
    # Retrieve the top 5 only - or all if less than 5.
    # Place the list in our context_dict dictionary which will be passed to the template engine.
    # that will be passed to the template engine.
    category_list = Category.objects.order_by('-likes')[:5]
    
    page_list = Page.objects.order_by('-views')[:5]
    
    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list
    
    # Render the response and send it back!
    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    
    context_dict = {'author':'Boyang An'}
    print(request.method)
    print(request.user)
    return render(request, 'rango/about.html', context=context_dict)

def about(request):
    return HttpResponse('Rango says: Here is the about page. <a href="/rango/">Index</a>')

def add_category(request):
    form = CategoryForm()
    
    
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        
        
        if form.is_valid():
            
            form.save(commit=True)
            return redirect('/rango/')
        else:
            print(form.errors)
    
    
    return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
        
    if category is None:
        return redirect('/rango/')
        
    form = PageForm()
    
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid() and category:
            page = form.save(commit=False)
            page.category = category
            page.views = 0
            page.save()
            return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors)
            
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)