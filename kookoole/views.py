 
 
from os import name
from pickle import NONE
from django.http import HttpResponse
from django.shortcuts import render ,redirect
from django.contrib.auth.hashers import make_password , check_password
from kookooleShop.models import Product
from kookooleShop.models import Categories
from kookooleShop.models import CustomerPin
from kookooleShop.models import CustomerLogUp
from kookooleShop.models import Order
from kookooleShop.middlewares.auth import auth_middleware
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator


        
  

def shopPage(request):
#methods manage ment
 post=request.method =='POST'
 get=request.method =='GET'
  
 if  get:
     #if kooky deleted error handeled(if cart not exists it through error) creating empty cart to overcome the error
    cart = request.session.get('cart')
    if not cart:
        request.session['cart']={}
    # end 
    all_products = None
     
    all_categories = Categories.get_all_categories();
    categoryID = request.GET.get('category')
    if categoryID:
        all_products = Product.get_all_products_by_category_id(categoryID);
        finaldata = all_products
        
        
    else:
         

        all_products = Product.get_all_products();

        #adding pagination
        paginator= Paginator(all_products, 6)
        page_number=request.GET.get('page')
        finaldata=paginator.get_page(page_number)
         
        #end pagination
       

    data ={}
     
    data['products'] = finaldata
    data['categories'] = all_categories
     
     
    print('you are :',request.session.get('email'))
     

    return render(request,'shop.html' , data)


 if  post:
     error_massage= None
     id =request.POST.get('id')
     stock=request.POST.get('stock')
     #print(id)
     cart = request.session.get('cart')
     
     if cart:
         quantity = cart.get(id)
         if quantity:
             if 'minus' in request.POST:
                 if quantity<=1:
                     cart.pop(id)
                 else:
  
                   cart[id] =quantity-1

             elif 'plus' in request.POST:
                 if quantity >=int(stock):
                     error_massage="quantity not available"
                 else:
                   cart[id] =quantity+1
               
         else:
             cart[id] = 1

     else:
         cart ={}
         cart[id] = 1

     request.session['cart'] = cart
     print(request.session['cart'])

     
     
     if  get:
     #if kooky deleted error handeled(if cart not exists it through error) creating empty cart to overcome the error
      cart = request.session.get('cart')
     if not cart:
        request.session['cart']={}
    # end 
     all_products = None
     
     all_categories = Categories.get_all_categories();
     categoryID = request.GET.get('category')
     if categoryID:
        all_products = Product.get_all_products_by_category_id(categoryID);
        finaldata = all_products
        
        
     else:
         

        all_products = Product.get_all_products();

        #adding pagination
        paginator= Paginator(all_products, 6)
        page_number=request.GET.get('page')
        finaldata=paginator.get_page(page_number)
         
        #end pagination
       

     data ={}
     
     data['products'] = finaldata
     data['categories'] = all_categories
     data['error'] = error_massage
     
     
     print('you are :',request.session.get('email'))
     

     return render(request,'shop.html' , data)


  
 
 
# handelling GET and POST method for signup page


def signupPage(request):
 #methods manage ment
 post=request.method =='POST'
 get=request.method =='GET'
 
 if  get:


        return render(request,"signup.html")
 if post:
        postData = request.POST
        first_name = postData.get('Firstname')
        last_name =  postData.get('Lastname')
        email =  postData.get('Email')
        password = postData.get('Password')
        phone = postData.get('Phone')
        pin = postData.get('Pin')
        
        

        #to see the inserted value in text field we have to store value dictionary

        value ={
            'first_name':first_name ,
            'last_name'  :last_name ,
            'email' :email ,
            'phone' :phone ,
            'pin' :pin  ,
            
            }
        

        error_message = None
         

        # loading data in customer oject it will be registered (stored) in data base
        customer = CustomerLogUp(first_name=first_name ,
                                 last_name=last_name ,
                                 email=email ,
                                 password=password, 
                                 phone=phone,
                                 pin=pin )



        #validatting(it is optional in sever side it can be validated in front end side also)

        if not first_name:
            error_message ="First Name Required !!!"
        elif len(first_name) < 1:
            error_message ="First Name Must Be 1 Char Long !!"


        elif not last_name:
            error_message ="Last Name Required !!!"
        elif len(last_name) < 2:
            error_message ="Last Name Must Be 2 Char Long !!"


        elif not email:
            error_message ="Email Required !!!"
        elif len(email) < 5:
            error_message ="Email Must Be 5 Char Long !!"
         

        # email already exist in data base true
        elif customer.isExists():
            error_message ="Email    Already     Exist   Please Login   or use another email ID !!"


        elif not password:
            error_message ="Password Required !!!"
        elif len(password) < 5:
            error_message ="Password Must Be 5 Char Long !!"

        
        elif not phone:
            error_message ="phone Required !!!"
        elif len(phone) < 10:
            error_message ="phone Number Must Be 10 Char Long !!"


        elif not pin:
            error_message ="Pin Required !!!"

        elif len(pin) != 6 : 
            error_message ="Pin Must be Six Charector"

        elif pin not in ['754109'] : 
            
            error_message ="We Are Not Giving Services To This Pin"
            
 
        # loaded data in customer oject will be registered in data base

        if not error_message:
            customer.password =make_password(customer.password)#hashing password
 
           
            customer.register()#("cussessfuly registered in database") 
            return redirect('homePage')


        else:

 # return render(request ,'signup.html' ,{'error' : error_message})# this error will be show in signupPage html using{%if error%}.alert.{%endif%}
           data={
               'error' : error_message ,
               'values' : value 
               #this 'value' holds the data inserted in signup form which is in above 
               #in html page we use values to show the inseted data

               }
            
           return render(request ,'signup.html' ,data)

def loginPage(request):

    if request.method =='GET':
        return render(request , 'login.html')
    else:
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email , password)
        customer = CustomerLogUp.get_customer_by_email(email)
        error_message= None
  
      
        print(email ,password)
        if customer:
         fla = check_password(password ,customer.password)
         if fla:
             request.session['customer_id'] = customer.id
             request.session['email'] = customer.email
              
             return redirect('homePage')
         else:
             error_message='invalid email or password !!!'
       
        else:
            error_message='invalid email or password !!!'
         
         
        
        return render(request , "login.html" ,{'error': error_message})


def Logout(request):
        request.session.clear()
        return redirect("/log-in/")


def Cart(request):
    if request.method =='GET':
    #showing session  cart item  in html cart icon
     ids =list(request.session.get('cart').keys())
     s_products =Product.get_products_by_id(ids)
     print(s_products)

     return render(request,"cart.html" ,{'s_products' :s_products})

    



    if request.method =='POST':
         
         
        id =request.POST.get('id')
        stock=request.POST.get('stock')
        
      
    cart = request.session.get('cart')
     
    if cart:
         quantity = cart.get(id)
         if quantity:
             
             if 'minus' in request.POST:
                 if quantity<=1:
                     cart.pop(id)
             
                 else:
  
                   cart[id] =quantity-1


             
             if 'pluse' in request.POST:
                    if quantity >=int(stock):
                     error_massage="quantity not available"
                    else:
                      cart[id] =quantity+1



             if 'remove' in request.POST:
                 cart.pop(id)
         else:
             cart[id] = 1

    else:
         cart ={}
         cart[id] = 1

    request.session['cart'] = cart
    print(request.session['cart'])
     
    return redirect("/cart-in/")
    #return render(request , "cart.html" ,{'error': error_sms})


def CheckOut(request):
    
     if request.method =='POST':

        print(request.POST)
         
        address = request.POST.get('Address')
        phone =  request.POST.get('Phone')
        customer = request.session.get('customer_id')
        cart = request.session.get('cart')
        products = Product.get_products_by_id(list(cart.keys()))
        print(address , phone ,customer ,cart ,products,)
      
        for product in products:
            order = Order(customer = CustomerLogUp(id = customer ) ,
                          product = product ,
                          price = product.price ,

                          address = address ,
                          phone = phone ,
                          quantity = cart.get(str(product.id)),
                          stock =product.stock
                          
                              )
            order.save()
             
            request.session['cart'] = {}


            ordersdata=Order.objects.all()
            for i in ordersdata :
                product_id=i.product_id
                order_quantity=i.quantity
                stock=i.stock
                curent_stock=stock - order_quantity
                print(order_quantity,stock,product_id,curent_stock)
                 
                Product.objects.filter(id=product_id).update(stock=curent_stock)

 


        return redirect("/thanks/")
      

def OrdersStatus(request):
    if request.method =='GET':
        customer = request.session.get('customer_id')
        orders = Order.get_orders_by_customer(customer)
        print(orders)
         
        return render(request ,'ordersstatus.html' ,{'orders': orders})


def Cancelation(request):
    if request.method =='GET':
        customer = request.session.get('customer_id')
        orders = Order.get_orders_by_customer(customer)
        print(orders)
         
        return render(request ,'manageorders.html' ,{'orders': orders})
    if request.method =='POST':
        cancel = False
        ids =  request.POST.get('id')
        order_quantity = request.POST.get('q')
        product_id=request.POST.get('product_id')
        available_stock =request.POST.get('stock')
        current_stock= int(available_stock)+ int(order_quantity)
        
        print(ids)
        Order.objects.filter(id=ids).update(cancelation=cancel)
     
        Product.objects.filter(id=product_id).update(stock=current_stock)
        
         
        return redirect("/manage-orders/")


def Search(request):
    post=request.method =='POST'
    get=request.method =='GET'
    query= request.GET['query']
    
    #allproducts= Product.objects.all()
    allproducts= Product.objects.filter(name__icontains=query)
    data ={'products': allproducts 
            
           }

    if  post:
     error_massage= None
     id =request.POST.get('id')
     stock=request.POST.get('stock')
     
     #print(id)
     cart = request.session.get('cart')
     
     if cart:
         quantity = cart.get(id)
         if quantity:
             if 'minus' in request.POST:
                 if quantity<=1:
                     cart.pop(id)
                 else:
  
                   cart[id] =quantity-1
             elif 'plus' in request.POST:
                 if quantity >=int(stock):
                     error_massage="quantity not available"
                 else:
                   cart[id] =quantity+1
               
         else:
             cart[id] = 1

     else:
         cart ={}
         cart[id] = 1

     request.session['cart'] = cart
     print(request.session['cart'])
 

    return render(request,'search.html', data)


def Thanks(request):

    return render(request,'thankyou.html')
    


     

   
