from django.shortcuts import render,redirect
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate

# Create your views here.

#-------------------------General(Dashboards,Widgets & Layout)---------------------------------------

# #---------------Dashboards

@login_required(login_url="/login_home")
def index(request):
    context = { "breadcrumb":{"parent":"Dashboard","child":"Default"},}
    return render(request,'index.html',context)

@login_required(login_url="/login_home")
def dashboard_02(request):
    context = { "breadcrumb":{"parent":"Dashboard", "child":"Project"}} 
    return render(request,"general/dashboard/project/dashboard-02.html",context)

@login_required(login_url="/login_home")
def dashboard_03(request):
    context = { "breadcrumb":{"parent":"Dashboard", "child":"Ecommerce"}} 
    return render(request,"general/dashboard/ecommerce/dashboard-03.html",context)

@login_required(login_url="/login_home")
def dashboard_04(request):
    context = { "breadcrumb":{"parent":"Dashboard", "child":"Education"}} 
    return render(request,"general/dashboard/education/dashboard-04.html",context)


# #---------------Widgets

@login_required(login_url="/login_home")
def general_widget(request):
    context = { "breadcrumb":{"parent":"Widgets", "child":"General"}} 
    return render(request,"general/widget/general-widget/general-widget.html",context)

@login_required(login_url="/login_home")
def chart_widget(request):
    context = { "breadcrumb":{"parent":"Widgets", "child":"Chart"}} 
    return render(request,"general/widget/chart-widget/chart-widget.html",context)


# #-----------------Layout
@login_required(login_url="/login_home")
def box_layout(request):
    context = {'layout':'box-layout', "breadcrumb":{"parent":"Page Layout", "child":"Box Layout"}}
    return render(request,"general/page-layout/box-layout.html",context)

@login_required(login_url="/login_home")
def layout_rtl(request):
    context = {'layout':'rtl', "breadcrumb":{"parent":"Page Layout", "child":"RTL Layout"}}
    return render(request,"general/page-layout/layout-rtl.html",context)

@login_required(login_url="/login_home")
def layout_dark(request):
    context = {'layout':'dark-only', "breadcrumb":{"parent":"Page Layout", "child":"Layout Dark"}}
    return render(request,"general/page-layout/layout-dark.html",context)

@login_required(login_url="/login_home")
def hide_on_scroll(request):
    context = { "breadcrumb":{"parent":"Page Layout", "child":"Hide Menu On Scroll"}}
    return render(request,"general/page-layout/hide-on-scroll.html",context)
    
#--------------------------------Applications---------------------------------

#---------------------Project 
@login_required(login_url="/login_home")
def projects(request):
    context = { "breadcrumb":{"parent":"Project", "child":"Project List"}}
    return render(request,"applications/projects/projects-list/projects.html",context)
    
@login_required(login_url="/login_home")
def projectcreate(request):
    context = { "breadcrumb":{"parent":"Apps", "child":"Project Create"}}
    return render(request,"applications/projects/projectcreate/projectcreate.html",context)


#-------------------File Manager
@login_required(login_url="/login_home")
def file_manager(request):
    context = { "breadcrumb":{"parent":"Apps", "child":"File Manager"}}
    return render(request,"applications/file-manager/file-manager.html",context)

#------------------------Kanban Board
@login_required(login_url="/login_home")
def kanban(request):
    context = { "breadcrumb":{"parent":"Apps", "child":"Kanban Board"}}
    return render(request,"applications/kanban/kanban.html",context)

#------------------------ ecommerce
@login_required(login_url="/login_home")
def add_products(request):
    context = { "breadcrumb":{"parent":"ECommerce", "child":"Add Products"}}
    return render(request,"applications/ecommerce/add-products/add-products.html",context)

@login_required(login_url="/login_home")
def product_cards(request):
    context = { "breadcrumb":{"parent":"Ecommerce", "child":"Product"}}
    return render(request,"applications/ecommerce/product/product.html",context)

@login_required(login_url="/login_home")
def product_page(request):
    context = { "breadcrumb":{"parent":"Ecommerce", "child":"Product Page"}}
    return render(request,"applications/ecommerce/product-page/product-page.html",context)

@login_required(login_url="/login_home")
def list_products(request):
    context = { "breadcrumb":{"parent":"Ecommerce", "child":"Product List"}}
    return render(request,"applications/ecommerce/list-products/list-products.html",context)

@login_required(login_url="/login_home")
def payment_details(request):
    context = { "breadcrumb":{"parent":"Ecommerce", "child":"Payment Details"}}
    return render(request,"applications/ecommerce/payment-details/payment-details.html",context)

@login_required(login_url="/login_home")
def order_history(request):
    context = { "breadcrumb":{"parent":"Ecommerce", "child":"Recent Orders"}}
    return render(request,"applications/ecommerce/order-history/order-history.html",context)
           
@login_required(login_url="/login_home")           
def invoice_1(request):
    return render(request,"applications/ecommerce/invoice-template/invoice-1.html")

@login_required(login_url="/login_home")
def invoice_2(request):
    return render(request,"applications/ecommerce/invoice-template/invoice-2.html")

@login_required(login_url="/login_home")
def invoice_3(request):
    return render(request,"applications/ecommerce/invoice-template/invoice-3.html")

@login_required(login_url="/login_home")
def invoice_4(request):
    return render(request,"applications/ecommerce/invoice-template/invoice-4.html")

@login_required(login_url="/login_home")
def invoice_5(request):
    return render(request,"applications/ecommerce/invoice-template/invoice-5.html")

@login_required(login_url="/login_home")
def invoice_template(request):
    context = { "breadcrumb":{"parent":"Ecommerce", "child":"Invoice-6"}}
    return render(request,"applications/ecommerce/invoice-template/invoice-template.html",context)

@login_required(login_url="/login_home")
def cart(request):
    context = { "breadcrumb":{"parent":"Ecommerce", "child":"Cart"}}
    return render(request,"applications/ecommerce/cart/cart.html",context)
      
@login_required(login_url="/login_home")
def list_wish(request):
    context = { "breadcrumb":{"parent":"Ecommerce", "child":"Wishlist"}}
    return render(request,"applications/ecommerce/list-wish/list-wish.html",context)
     
@login_required(login_url="/login_home")
def checkout(request):
    context = { "breadcrumb":{"parent":"Ecommerce", "child":"Checkout"}}
    return render(request,"applications/ecommerce/checkout/checkout.html",context)
    
@login_required(login_url="/login_home")
def pricing(request):
    context = { "breadcrumb":{"parent":"Ecommerce", "child":"Pricing"}}
    return render(request,"applications/ecommerce/pricing/pricing.html",context)


#------------------------ Letter-Box
@login_required(login_url="/login_home")
def letter_box(request):
    context = { "breadcrumb":{"parent":"Email", "child":"Letter Box"}}
    return render(request,"applications/letter-box/letter-box.html",context)

#--------------------------------chat
@login_required(login_url="/login_home")
def private_chat(request):
    context = { "breadcrumb":{"parent":"Chat", "child":"Private Chat"}}
    return render(request,"applications/chat/private-chat/private-chat.html",context)
     
@login_required(login_url="/login_home")
def group_chat(request):
    context = { "breadcrumb":{"parent":"Chat", "child":"Group Chat"}}
    return render(request,"applications/chat/group-chat/group-chat.html",context)



#---------------------------------user
@login_required(login_url="/login_home")
def user_profile(request):
    context = { "breadcrumb":{"parent":"Users", "child":"User Profile"}}
    return render(request,"applications/user/user-profile/user-profile.html",context)
    
@login_required(login_url="/login_home")
def edit_profile(request):
    context = { "breadcrumb":{"parent":"Users", "child":"Edit Profile"}}
    return render(request,"applications/user/edit-profile/edit-profile.html",context)
       
@login_required(login_url="/login_home")
def user_cards(request):
    context = { "breadcrumb":{"parent":"Users", "child":"User Cards"}}
    return render(request,"applications/user/user-cards/user-cards.html",context)


#------------------------bookmark
@login_required(login_url="/login_home")
def bookmark(request):
    context = { "breadcrumb":{"parent":"Apps", "child":"Bookmarks"}}
    return render(request,"applications/bookmark/bookmark.html",context)


#------------------------contacts
@login_required(login_url="/login_home")
def contacts(request):
    context = { "breadcrumb":{"parent":"Apps", "child":"Contacts"}}
    return render(request,"applications/contacts/contacts.html",context)


#------------------------task
@login_required(login_url="/login_home")
def task(request):
    context = { "breadcrumb":{"parent":"Apps", "child":"Tasks"}}
    return render(request,"applications/task/task.html",context)
    

#------------------------calendar
@login_required(login_url="/login_home")
def calendar_basic(request):
    context = { "breadcrumb":{"parent":"Apps", "child":"Calender Basic"}}
    return render(request,"applications/calendar/calendar-basic.html",context)
    

#------------------------social-app
@login_required(login_url="/login_home")
def social_app(request):
    context = { "breadcrumb":{"parent":"Apps", "child":"Social App"}}
    return render(request,"applications/social-app/social-app.html",context)


#------------------------to-do
@login_required(login_url="/login_home")
def to_do(request):
    context = { "breadcrumb":{"parent":"Apps", "child":"To-Do"}}
    return render(request,"applications/to-do/to-do.html",context)
    

#------------------------search
@login_required(login_url="/login_home")
def search(request):
    context = { "breadcrumb":{"parent":"Search Pages", "child":"Search Website"}}
    return render(request,"applications/search/search.html",context)



#--------------------------------Forms & Table-----------------------------------------------
#--------------------------------Forms------------------------------------
#------------------------form-controls

@login_required(login_url="/login_home")
def form_validation(request):
    context = { "breadcrumb":{"parent":"Form Controls", "child":"Validation Form"}}
    return render(request,"forms-table/forms/form-controls/form-validation/form-validation.html",context)


@login_required(login_url="/login_home")
def base_input(request):
    context = { "breadcrumb":{"parent":"Form Controls", "child":"Base Inputs"}}
    return render(request,"forms-table/forms/form-controls/base-input/base-input.html",context)    


@login_required(login_url="/login_home")
def radio_checkbox_control(request):
    context = { "breadcrumb":{"parent":"Form Controls", "child":"Checkbox & Radio"}}
    return render(request,"forms-table/forms/form-controls/radio-checkbox-control/radio-checkbox-control.html",context)
    
    
@login_required(login_url="/login_home")
def input_group(request):
    context = { "breadcrumb":{"parent":"Form Controls", "child":"Input Groups"}}
    return render(request,"forms-table/forms/form-controls/input-group/input-group.html",context)


@login_required(login_url="/login_home")
def input_mask(request):
    context = { "breadcrumb":{"parent":"Form Controls", "child":"Input Mask"}}
    return render(request,"forms-table/forms/form-controls/input-mask/input-mask.html",context)
    
    
@login_required(login_url="/login_home")
def megaoptions(request):
    context = { "breadcrumb":{"parent":"Form Controls", "child":"Mega Options"}}
    return render(request,"forms-table/forms/form-controls/megaoptions/megaoptions.html",context)    



#---------------------------form widgets

@login_required(login_url="/login_home")
def datepicker(request):
    context = { "breadcrumb":{"parent":"Form Widgets", "child":"Datepicker"}}
    return render(request,"forms-table/forms/form-widgets/datepicker/datepicker.html",context)


@login_required(login_url="/login_home")    
def touchspin(request):
    context = { "breadcrumb":{"parent":"Form Widgets", "child":"Touchspin"}}
    return render(request,'forms-table/forms/form-widgets/touchspin/touchspin.html',context)


@login_required(login_url="/login_home")
def select2(request):
    context = { "breadcrumb":{"parent":"Form Widgets", "child":"Select2"}}
    return render(request,'forms-table/forms/form-widgets/select2/select2.html',context)


@login_required(login_url="/login_home")      
def switch(request):
    context = { "breadcrumb":{"parent":"Form Widgets", "child":"Switch"}}
    return render(request,'forms-table/forms/form-widgets/switch/switch.html',context)
      

@login_required(login_url="/login_home")      
def typeahead(request):
    context = { "breadcrumb":{"parent":"Form Widgets", "child":"Typeahead"}}
    return render(request,'forms-table/forms/form-widgets/typeahead/typeahead.html',context)
      

@login_required(login_url="/login_home")    
def clipboard(request):
    context = { "breadcrumb":{"parent":"Form Widgets", "child":"Clipboard"}}
    return render(request,'forms-table/forms/form-widgets/clipboard/clipboard.html',context)
     
     
#-----------------------form layout

@login_required(login_url="/login_home")
def form_wizard_one(request):
    context = { "breadcrumb":{"parent":"Form Layout", "child":"Form Wizard"}}
    return render(request,'forms-table/forms/form-layout/form-wizard/form-wizard.html',context) 


@login_required(login_url="/login_home")
def form_wizard_two(request):
    context = { "breadcrumb":{"parent":"Form Layout", "child":"Step Form Wizard"}}
    return render(request,'forms-table/forms/form-layout/form-wizard-two/form-wizard-two.html',context) 


@login_required(login_url="/login_home")
def two_factor(request):
    context = { "breadcrumb":{"parent":"Form Layout", "child":"Two Factor"}}
    return render(request,'forms-table/forms/form-layout/two-factor/two-factor.html',context)



#----------------------------------------------------Table------------------------------------------
#------------------------bootstrap table

@login_required(login_url="/login_home")
def basic_table(request):
    context = { "breadcrumb":{"parent":"Bootstrap Tables", "child":"Bootstrap Basic Tables"}}
    return render(request,'forms-table/table/bootstrap-table/basic-table/bootstrap-basic-table.html',context)
    

@login_required(login_url="/login_home")
def table_components(request):
    context = { "breadcrumb":{"parent":"Bootstrap Tables", "child":"Table Components"}}
    return render(request,'forms-table/table/bootstrap-table/table-components/table-components.html',context)


#------------------------data table

@login_required(login_url="/login_home")
def datatable_basic_init(request):
    context = { "breadcrumb":{"parent":"Data Tables", "child":"Basic DataTables"}}
    return render(request,'forms-table/table/data-table/datatable-basic/datatable-basic-init.html',context)
    

@login_required(login_url="/login_home")
def datatable_advance(request):
    context = { "breadcrumb":{"parent":"Data Tables", "child":"Advance Init"}}
    return render(request,'forms-table/table/data-table/datatable-advance/datatable-advance.html',context)
    

@login_required(login_url="/login_home")
def datatable_API(request):
    context = { "breadcrumb":{"parent":"Data Tables", "child":"API DataTables"}}
    return render(request,'forms-table/table/data-table/datatable-API/datatable-API.html',context)
    

@login_required(login_url="/login_home")
def datatable_data_source(request):
    context = { "breadcrumb":{"parent":"Data Tables", "child":"DATA Source DataTables"}}
    return render(request,'forms-table/table/data-table/data-source/datatable-data-source.html',context)


#-------------------------------EX.data-table

@login_required(login_url="/login_home")
def ext_autofill(request):
    context = { "breadcrumb":{"parent":"Extension Data Tables", "child":"Autofill Datatables"}}
    return render(request,'forms-table/table/Ex-data-table/ext-autofill/datatable-ext-autofill.html',context)


#--------------------------------jsgrid_table

@login_required(login_url="/login_home")
def jsgrid_table(request):
    context = { "breadcrumb":{"parent":"Tables", "child":"JS Grid Tables"}}
    return render(request,'forms-table/table/js-grid-table/jsgrid-table.html',context) 



#------------------Components------UI Components-----Elements ----------->

#-----------------------------Ui kits

@login_required(login_url="/login_home")
def typography(request):
    context = { "breadcrumb":{"parent":"Ui Kits", "child":"Typography"}}
    return render(request,'components/ui-kits/typography.html', context)


@login_required(login_url="/login_home")
def avatars(request):
    context = { "breadcrumb":{"parent":"Ui Kits", "child":"Avatars"}}
    return render(request,'components/ui-kits/avatars.html', context)
     

@login_required(login_url="/login_home")
def helper_classes(request):
    context = { "breadcrumb":{"parent":"Ui Kits", "child":"Helper Classes"}}
    return render(request,'components/ui-kits/helper-classes.html', context)


@login_required(login_url="/login_home")
def grid(request):
    context = { "breadcrumb":{"parent":"Ui Kits", "child":"Grid"}}
    return render(request,'components/ui-kits/grid.html', context)


@login_required(login_url="/login_home")      
def tagpills(request):
    context = { "breadcrumb":{"parent":"Ui Kits", "child":"Tag & Pills"}}
    return render(request,'components/ui-kits/tag-pills.html', context)
      
      
@login_required(login_url="/login_home")
def progressbar(request):
    context = { "breadcrumb":{"parent":"Ui Kits", "child":"Progress"}}
    return render(request,'components/ui-kits/progress-bar.html', context)
     
         
@login_required(login_url="/login_home")
def modal(request):
    context = { "breadcrumb":{"parent":"Ui Kits", "child":"Modal"}}
    return render(request,'components/ui-kits/modal.html', context)  

    
@login_required(login_url="/login_home")
def alert(request):
    context = { "breadcrumb":{"parent":"Ui Kits", "child":"Alert"}}
    return render(request,'components/ui-kits/alert.html', context)
    
    
@login_required(login_url="/login_home")   
def popover(request):
    context = { "breadcrumb":{"parent":"Ui Kits", "child":"Popover"}}
    return render(request,'components/ui-kits/popover.html', context) 
    
    
@login_required(login_url="/login_home")
def tooltip(request):
    context = { "breadcrumb":{"parent":"Ui Kits", "child":"Tooltip"}}
    return render(request,'components/ui-kits/tooltip.html', context)
    
    
@login_required(login_url="/login_home")
def dropdown(request):
    context = { "breadcrumb":{"parent":"Ui Kits", "child":"Dropdown"}}
    return render(request,'components/ui-kits/dropdown.html', context)   
    
    
@login_required(login_url="/login_home")
def accordion(request):
    context = { "breadcrumb":{"parent":"Ui Kits", "child":"Accordion"}}
    return render(request,'components/ui-kits/according.html', context)    
    
    
@login_required(login_url="/login_home")
def bootstraptab(request):
    context = { "breadcrumb":{"parent":"Ui Kits", "child":"Bootstrap Tabs"}}
    return render(request,'components/ui-kits/tab-bootstrap.html', context)    


@login_required(login_url="/login_home")
def lists(request):
    context = {"breadcrumb":{"parent":"Ui Kits", "child":"Lists"}}
    return render(request,'components/ui-kits/list.html', context) 



#-------------------------------Bonus Ui

@login_required(login_url="/login_home")
def scrollable(request):
    context = {"breadcrumb":{"parent":"Bonus Ui", "child":"Scrollable"}}
    return render(request,'components/bonus-ui/scrollable.html', context)
            
            
@login_required(login_url="/login_home")
def tree(request):
    context = {"breadcrumb":{"parent":"Bonus Ui", "child":"Tree View"}}
    return render(request,'components/bonus-ui/tree.html', context)


@login_required(login_url="/login_home")           
def toasts(request):
    context = {"breadcrumb":{"parent":"Bonus Ui", "child":"Toasts"}}
    return render(request,'components/bonus-ui/toasts.html', context)      

  
@login_required(login_url="/login_home")    
def rating(request):
    context = {"breadcrumb":{"parent":"Bonus Ui", "child":"Rating"}}
    return render(request,'components/bonus-ui/rating.html', context)
               
               
@login_required(login_url="/login_home")
def dropzone(request):
    context = {"breadcrumb":{"parent":"Bonus Ui", "child":"Dropzone"}}
    return render(request,'components/bonus-ui/dropzone.html', context)    
    
    
@login_required(login_url="/login_home")
def tour(request):
    context = {"breadcrumb":{"parent":"Bonus Ui", "child":"Tour"}}
    return render(request,'components/bonus-ui/tour.html', context)        
    
    
@login_required(login_url="/login_home")
def sweetalert2(request):
    context = {"breadcrumb":{"parent":"Bonus Ui", "child":"Sweet Alert"}}
    return render(request,'components/bonus-ui/sweet-alert2.html', context)    
    
    
@login_required(login_url="/login_home")
def animatedmodal(request):
    context = {"breadcrumb":{"parent":"Bonus Ui", "child":"Animated Modal"}}
    return render(request,'components/bonus-ui/modal-animated.html', context)     
    
    
@login_required(login_url="/login_home")
def owlcarousel(request):
    context = {"breadcrumb":{"parent":"Bonus Ui", "child":"Owl Carousel"}}
    return render(request,'components/bonus-ui/owl-carousel.html', context)
    
              
@login_required(login_url="/login_home")
def ribbons(request):
    context = {"breadcrumb":{"parent":"Bonus Ui", "child":"Ribbons"}}
    return render(request,'components/bonus-ui/ribbons.html', context) 
    
             
@login_required(login_url="/login_home")
def pagination(request):
    context = {"breadcrumb":{"parent":"Bonus Ui", "child":"Paginations"}}
    return render(request,'components/bonus-ui/pagination.html', context)
      
        
@login_required(login_url="/login_home")
def breadcrumb(request):
    context = {"breadcrumb":{"parent":"Bonus Ui", "child":"Breadcrumb"}}
    return render(request,'components/bonus-ui/breadcrumb.html', context)       
    
    
@login_required(login_url="/login_home")
def rangeslider(request):
    context = {"breadcrumb":{"parent":"Bonus Ui", "child":"Range Slider"}}
    return render(request,'components/bonus-ui/range-slider.html', context)     
    
    
@login_required(login_url="/login_home")
def imagecropper(request):
    context = {"breadcrumb":{"parent":"Bonus Ui", "child":"Image Cropper"}}
    return render(request,'components/bonus-ui/image-cropper.html', context)      
    

@login_required(login_url="/login_home")
def basiccard(request):
    context = {"breadcrumb":{"parent":"Bonus Ui", "child":"Basic Card"}}
    return render(request,'components/bonus-ui/basic-card.html', context)
                    
                    
@login_required(login_url="/login_home")
def creativecard(request):
    context = {"breadcrumb":{"parent":"Bonus Ui", "child":"Creative Card"}}
    return render(request,'components/bonus-ui/creative-card.html', context)  
       

@login_required(login_url="/login_home")
def draggablecard(request):
    context = {"breadcrumb":{"parent":"Bonus Ui", "child":"Draggable Card"}}
    return render(request,'components/bonus-ui/dragable-card.html', context)       
    
    
@login_required(login_url="/login_home")    
def timeline1(request):
    context = {"breadcrumb":{"parent":"Bonus Ui", "child":"Range Slider"}}
    return render(request,'components/bonus-ui/timeline-v-1.html', context)        
    


#---------------------------------Animation

@login_required(login_url="/login_home")
def animate(request):
    context = {"breadcrumb":{"parent":"Animation", "child":"Animate"}}
    return render(request,'components/animation/animate.html', context)
            
            
@login_required(login_url="/login_home")
def scrollreval(request):
    context = {"breadcrumb":{"parent":"Animation", "child":"Scroll Reveal"}}
    return render(request,'components/animation/scroll-reval.html', context)        
    

@login_required(login_url="/login_home")
def AOS(request):
    context = {"breadcrumb":{"parent":"Animation", "child":"AOS Animation"}}
    return render(request,'components/animation/AOS.html', context)
            

@login_required(login_url="/login_home")
def tilt(request):
    context = {"breadcrumb":{"parent":"Animation", "child":"Tilt Animation"}}
    return render(request,'components/animation/tilt.html', context)        
    
    
@login_required(login_url="/login_home")
def wow(request):
    context = {"breadcrumb":{"parent":"Animation", "child":"Wow Animation"}}
    return render(request,'components/animation/wow.html', context)    



#--------------------------Icons

@login_required(login_url="/login_home")
def flagicon(request):
    context = {"breadcrumb":{"parent":"Icons", "child":"Flag Icons"}}
    return render(request,'components/icons/flag-icon.html', context) 
    

@login_required(login_url="/login_home")
def fontawesome(request):
    context = {"breadcrumb":{"parent":"Icons", "child":"Font Awesome Icon"}}
    return render(request,'components/icons/font-awesome.html', context) 
    

@login_required(login_url="/login_home")
def icoicon(request):
    context = {"breadcrumb":{"parent":"Ui Kits", "child":"ICO Icon"}}
    return render(request,'components/icons/ico-icon.html', context) 
    
    
@login_required(login_url="/login_home")
def themify(request):
    context = {"breadcrumb":{"parent":"Icons", "child":"Themify Icon"}}
    return render(request,'components/icons/themify-icon.html', context)  


@login_required(login_url="/login_home")    
def feather(request):
    context = {"breadcrumb":{"parent":"Icons", "child":"Feather Icons"}}
    return render(request,'components/icons/feather-icon.html', context)  
    
    
@login_required(login_url="/login_home")
def whether(request):
    context = {"breadcrumb":{"parent":"Icons", "child":"Whether Icon"}}
    return render(request,'components/icons/whether-icon.html', context)      



#--------------------------------Buttons

@login_required(login_url="/login_home")
def buttons(request):
    context = {"breadcrumb":{"parent":"Buttons", "child":"Default Style"}}
    return render(request,'components/buttons/buttons.html', context)        
       
       
@login_required(login_url="/login_home")
def flat(request):
    context = {"breadcrumb":{"parent":"Buttons", "child":"Flat Buttons"}}
    return render(request,'components/buttons/buttons-flat.html', context)      
       
       
@login_required(login_url="/login_home")
def edge(request):
    context = {"breadcrumb":{"parent":"Buttons", "child":"Edge Buttons"}}
    return render(request,'components/buttons/buttons-edge.html', context)
           
               
@login_required(login_url="/login_home")
def raised(request):
    context = {"breadcrumb":{"parent":"Buttons", "child":"Raised Buttons"}}
    return render(request,'components/buttons/raised-button.html', context)
          

@login_required(login_url="/login_home")
def group(request):
    context = {"breadcrumb":{"parent":"Buttons", "child":"Button Group"}}
    return render(request,'components/buttons/button-group.html', context)   



#-------------------------------charts

@login_required(login_url="/login_home")
def echarts(request):
    context = {"breadcrumb":{"parent":"Charts", "child":"Echarts"}}
    return render(request,'components/charts/echarts.html', context)
    

@login_required(login_url="/login_home")
def apex(request):
    context = {"breadcrumb":{"parent":"Charts", "child":"Apex Chart"}}
    return render(request,'components/charts/chart-apex.html', context)    
    
    
@login_required(login_url="/login_home")         
def google(request):
    context = {"breadcrumb":{"parent":"Charts", "child":"Google Chart"}}
    return render(request,'components/charts/chart-google.html', context)


@login_required(login_url="/login_home")         
def sparkline(request):
    context = {"breadcrumb":{"parent":"Charts", "child":"Sparkline Chart"}}
    return render(request,'components/charts/chart-sparkline.html', context)      


@login_required(login_url="/login_home")             
def flot(request):
    context = {"breadcrumb":{"parent":"Charts", "child":"Flot Chart"}}
    return render(request,'components/charts/chart-flot.html', context)   
    

@login_required(login_url="/login_home")
def knob(request):
    context = {"breadcrumb":{"parent":"Charts", "child":"Knob Chart"}}
    return render(request,'components/charts/chart-knob.html', context)     
       
       
@login_required(login_url="/login_home")         
def morris(request):
    context = {"breadcrumb":{"parent":"Charts", "child":"Morris Chart"}}
    return render(request,'components/charts/chart-morris.html', context)


@login_required(login_url="/login_home")      
def chartjs(request):
    context = {"breadcrumb":{"parent":"Charts", "child":"ChartJS Chart"}}
    return render(request,'components/charts/chartjs.html', context)     
    
    
@login_required(login_url="/login_home")
def chartist(request):
    context = {"breadcrumb":{"parent":"Charts", "child":"Chartist Chart"}}
    return render(request,'components/charts/chartist.html', context)   

         

@login_required(login_url="/login_home")
def peity(request):
    context = {"breadcrumb":{"parent":"Charts", "child":"Peity Chart"}}
    return render(request,'components/charts/chart-peity.html', context)     



#------------------------------------------Pages-------------------------------------

#-------------------------sample-page

@login_required(login_url="/login_home")
def sample_page(request):
    context = {"breadcrumb":{"parent":"Pages", "child":"Sample Page"}}    
    return render(request,'pages/sample-page/sample-page.html',context)
    
#--------------------------internationalization

@login_required(login_url="/login_home")
def internationalization(request):
    context = {"breadcrumb":{"parent":"Pages", "child":"Internationalization"}}
    return render(request,'pages/internationalization/internationalization.html',context)
    

#-----------------------------------------------others

# ------------------------------error page

@login_required(login_url="/login_home")
def error_400(request):
    return render(request,'pages/others/error-page/error-page/error-400.html')


@login_required(login_url="/login_home")
def error_401(request):
    return render(request,'pages/others/error-page/error-page/error-401.html')
    

@login_required(login_url="/login_home")
def error_403(request):
    return render(request,'pages/others/error-page/error-page/error-403.html')


@login_required(login_url="/login_home")
def error_404(request):
    return render(request,'pages/others/error-page/error-page/error-404.html')
    

@login_required(login_url="/login_home")
def error_500(request):
    return render(request,'pages/others/error-page/error-page/error-500.html')
    

@login_required(login_url="/login_home")
def error_503(request):
    return render(request,'pages/others/error-page/error-page/error-503.html')
    

#----------------------------------Authentication



@login_required(login_url="/login_home")
def login_simple(request):
    return render(request,'pages/others/authentication/login/login.html')


@login_required(login_url="/login_home")
def login_one(request):
    return render(request,'pages/others/authentication/login-one/login_one.html')
    

@login_required(login_url="/login_home")
def login_two(request):
    return render(request,'pages/others/authentication/login-two/login_two.html')


@login_required(login_url="/login_home")
def login_bs_validation(request):
    return render(request,'pages/others/authentication/login-bs-validation/login-bs-validation.html')


@login_required(login_url="/login_home")
def login_tt_validation(request):
    return render(request,'pages/others/authentication/login-bs-tt-validation/login-bs-tt-validation.html')
    

@login_required(login_url="/login_home")
def login_validation(request):
    return render(request,'pages/others/authentication/login-sa-validation/login-sa-validation.html')
    

@login_required(login_url="/login_home")
def sign_up(request):
    return render(request,'pages/others/authentication/sign-up/sign-up.html')  


@login_required(login_url="/login_home")
def sign_one(request):
    return render(request,'pages/others/authentication/sign-one/sign-up-one.html')
    

@login_required(login_url="/login_home")
def sign_two(request):
    return render(request,'pages/others/authentication/sign-two/sign-up-two.html')


@login_required(login_url="/login_home")
def sign_wizard(request):
    return render(request,'pages/others/authentication/sign-up-wizard/sign-up-wizard.html')    


@login_required(login_url="/login_home")
def unlock(request):
    return render(request,'pages/others/authentication/unlock/unlock.html')
    

@login_required(login_url="/login_home")
def forget_password(request):
    return render(request,'pages/others/authentication/forget-password/forget-password.html')
    

@login_required(login_url="/login_home")
def reset_password(request):
    return render(request,'pages/others/authentication/reset-password/reset-password.html')


@login_required(login_url="/login_home")
def maintenance(request):
    return render(request,'pages/others/authentication/maintenance/maintenance.html')



#---------------------------------------comingsoon

@login_required(login_url="/login_home")
def comingsoon(request):
    return render(request,'pages/others/comingsoon/comingsoon/comingsoon.html')
    

@login_required(login_url="/login_home")
def comingsoon_video(request):
    return render(request,'pages/others/comingsoon/comingsoon-video/comingsoon-bg-video.html')


@login_required(login_url="/login_home")
def comingsoon_img(request):
    return render(request,'pages/others/comingsoon/comingsoon-img/comingsoon-bg-img.html')
    

#----------------------------------Email-Template

@login_required(login_url="/login_home")
def basic_temp(request):
    return render(request,'pages/others/email-templates/basic-email/basic-template.html')
    

@login_required(login_url="/login_home")
def email_header(request):
    return render(request,'pages/others/email-templates/basic-header/email-header.html')
    

@login_required(login_url="/login_home")
def template_email(request):
    return render(request,'pages/others/email-templates/ecom-template/template-email.html')
    

@login_required(login_url="/login_home")
def template_email_2(request):
    return render(request,'pages/others/email-templates/template-email-2/template-email-2.html')


@login_required(login_url="/login_home")
def ecommerce_temp(request):
    return render(request,'pages/others/email-templates/ecom-email/ecommerce-templates.html')
    

@login_required(login_url="/login_home")
def email_order(request):
    return render(request,'pages/others/email-templates/order-success/email-order-success.html')     



#------------------------------------------Miscellaneous----------------- -------------------------

#--------------------------------------gallery

@login_required(login_url="/login_home")
def gallery_grid(request):
    context = {"breadcrumb":{"parent":"Gallery", "child":"Gallery"}}    
    return render(request,'miscellaneous/gallery/gallery-grid/gallery.html',context)
    


@login_required(login_url="/login_home")
def gallery_description(request):
    context = {"breadcrumb":{"parent":"Gallery", "child":"Gallery Grid With Description"}}    
    return render(request,'miscellaneous/gallery/gallery-grid-desc/gallery-with-description.html',context)
    


@login_required(login_url="/login_home")
def masonry_gallery(request):
    context = {"breadcrumb":{"parent":"Gallery", "child":"Masonry Gallery"}}    
    return render(request,'miscellaneous/gallery/masonry-gallery/gallery-masonry.html',context)
    


@login_required(login_url="/login_home")
def masonry_disc(request):
    context = {"breadcrumb":{"parent":"Gallery", "child":"Masonry Gallery With Description"}}    
    return render(request,'miscellaneous/gallery/masonry-with-desc/masonry-gallery-with-disc.html',context)
    


@login_required(login_url="/login_home")
def hover(request):
    context = {"breadcrumb":{"parent":"Gallery", "child":"Image Hover Effects"}}    
    return render(request,'miscellaneous/gallery/hover-effects/gallery-hover.html',context)
    
#------------------------------------Blog

@login_required(login_url="/login_home")
def blog_details(request):  
    context = {"breadcrumb":{"parent":"Blog", "child":"Blog Details"}}    
    return render(request,'miscellaneous/blog/blog-details/blog.html',context)
    


@login_required(login_url="/login_home")
def blog_single(request):
    context = {"breadcrumb":{"parent":"Blog", "child":"Blog Single"}}    
    return render(request,'miscellaneous/blog/blog-single/blog-single.html',context)
    


@login_required(login_url="/login_home")
def add_post(request):
    context = {"breadcrumb":{"parent":"Blog", "child":"Add Post"}}    
    return render(request,'miscellaneous/blog/add-post/add-post.html',context)
    
#--------------------------------------faq

@login_required(login_url="/login_home")
def FAQ(request):
    context = {"breadcrumb":{"parent":"FAQ", "child":"FAQ"}}    
    return render(request,'miscellaneous/FAQ/faq.html',context)


#---------------------------------job serach

@login_required(login_url="/login_home")
def job_cards(request):
    context = {"breadcrumb":{"parent":"Job Search", "child":"Cards View"}}    
    return render(request,'miscellaneous/job-search/cards-view/job-cards-view.html',context)
    

@login_required(login_url="/login_home")
def job_list(request):
    context = {"breadcrumb":{"parent":"Job Search", "child":"List View"}}    
    return render(request,'miscellaneous/job-search/list-view/job-list-view.html',context)
    

@login_required(login_url="/login_home")
def job_details(request):
    context = {"breadcrumb":{"parent":"Job Search", "child":"Job Details"}}    
    return render(request,'miscellaneous/job-search/job-details/job-details.html',context)
    

@login_required(login_url="/login_home")
def apply(request):
    context = {"breadcrumb":{"parent":"Job Search", "child":"Apply"}}    
    return render(request,'miscellaneous/job-search/apply/job-apply.html',context)
    
#------------------------------------Learning

@login_required(login_url="/login_home")
def learning_list(request):
    context = {"breadcrumb":{"parent":"Learning", "child":"Learning List"}}    
    return render(request,'miscellaneous/learning/learning-list/learning-list-view.html',context)
    

@login_required(login_url="/login_home")
def learning_detailed(request):
    context = {"breadcrumb":{"parent":"Learning", "child":"Detailed Course"}}    
    return render(request,'miscellaneous/learning/learning-detailed/learning-detailed.html',context)
    

#----------------------------------------Maps
@login_required(login_url="/login_home")
def maps_js(request):
    context = {"breadcrumb":{"parent":"Maps", "child":"Map JS"}}    
    return render(request,'miscellaneous/maps/maps-js/map-js.html',context)
    
   
@login_required(login_url="/login_home")
def vector_maps(request):
    context = {"breadcrumb":{"parent":"Maps", "child":"Vector Maps"}}
    return render(request,'miscellaneous/maps/vector-maps/vector-map.html',context)
    

#------------------------------------Editors
   
@login_required(login_url="/login_home")
def summernote(request):
    context = {"breadcrumb":{"parent":"Editors", "child":"Summer Note"}}    
    return render(request,'miscellaneous/editors/summer-note/summernote.html',context)
    

@login_required(login_url="/login_home")
def ckeditor(request):
    context = {"breadcrumb":{"parent":"Editors", "child":"Ck Editor"}}    
    return render(request,'miscellaneous/editors/ckeditor/ckeditor.html',context)
    

@login_required(login_url="/login_home")
def simple_mde(request):
    context = {"breadcrumb":{"parent":"Editors", "child":"MDE Editor"}}    
    return render(request,'miscellaneous/editors/simple-mde/simple-mde.html',context) 
    
    
@login_required(login_url="/login_home")
def ace_code(request):
    context = {"breadcrumb":{"parent":"Editors", "child":"ACE Code Editor"}}    
    return render(request,'miscellaneous/editors/ace-code/ace-code-editor.html',context) 
    
#----------------------------knowledgeUi Kits
@login_required(login_url="/login_home")
def knowledgebase(request):
    context = {"breadcrumb":{"parent":"Knowledgebase", "child":"Knowledgebase"}}    
    return render(request,'miscellaneous/knowledgebase/knowledgebase.html',context)
    
#-----------------------------support-ticket
@login_required(login_url="/login_home")
def support_ticket(request):
    context = { "breadcrumb":{"parent":"Apps", "child":"Support Ticket"}}
    return render(request,"miscellaneous/support-ticket/support-ticket.html",context)
      

#---------------------------------------------------------------------------------------



def signup_home(request):
    if request.method == "GET":
        return render(request, 'signup.html')
    else:
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.filter(email=email).exists()
        if user:
            raise Exception('Something went wrong')
        new_user = User.objects.create_user(username=username,email=email, password=password)
        new_user.save()
        return redirect('index')
    
    
def logout_view(request):
    logout(request)
    return redirect('login_home')


def login_home(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password  = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request,user)
                if 'next' in request.GET:
                    nextPage = request.GET['next']
                    return HttpResponseRedirect(nextPage)
                return redirect("index")
            else:
                messages.error(request,"Wrong credentials")
                return redirect("login_home")
        else:
            messages.error(request,"Wrong credentials")
            return redirect("login_home")
    else:
        form = AuthenticationForm()        
        
    return render(request,'main-login.html',{"form":form,})





         



       
    






