#coding=utf-8
# Create your views here.
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context 
from django.shortcuts import render_to_response

from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt 
from django.template import RequestContext  
from django import forms
from django.shortcuts import redirect



import datetime





#model

from ticket1.models import City
from ticket1.models import Route
from ticket1.models import Catalog
from ticket1.models import Order












def my_homepage_view(request):
#    now = datetime.datetime.now()
#   assert False
#    html = "<html><head>This is my super home page. </head> <body>It is now %s.</body></html>" % now
    values = request.META.items()
    values.sort()
    html = []
    for k, v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))
#    return HttpResponse(html)



#   ############################
def yearmonthdata_dash(date):
    return ''.join([date[0:3],'-',date[4:6],'-',date[6:9]])




def ticket1_main_query(request):

#    return render_to_response('main_query.html')
    return render_to_response('main_query.html', {}  ,context_instance=RequestContext(request))


class QueryForm(forms.Form):
    ddlOrgCity = forms.CharField()
    ddlDesCity = forms.CharField()
    control_date_from = forms.CharField()
    

#@csrf_exempt
def ticket1_order(request):
    if request.method == 'POST':
#        qform = QueryForm(request.POST)
#        if qform.is_valid():
        local_city_from = request.POST['ddlOrgCity']
        local_city_to = request.POST['ddlDesCity']
        local_city_from_date = request.POST['control_date_from']
        
        
        try:
            local_city_from_ID_o= City.objects.get(City_Name = local_city_from)
            local_city_to_ID_o = City.objects.get(City_Name = local_city_to)
        except City.DoesNotExist:
            local_city_from_ID = ''
            local_city_to_ID = ''
            print "Apress isn't in the database yet."
        else:
            local_city_from_ID = local_city_from_ID_o.City_ID
            local_city_to_ID = local_city_to_ID_o.City_ID
    

    
        #get route id
        try:
            local_route_id_o = Route.objects.get(Route_Start_City_ID=local_city_from_ID, Route_To_City_ID=local_city_to_ID)

        except Route.DoesNotExist:
            local_route_id = ''
        else:
            local_route_id = local_route_id_o.Route_ID
            
        #get route id
#        local_catalog_id_o = Catalog.objects.get(Catalog_Route_ID=local_route_id)
        local_catalog=[]
        try:
            local_catalog_id_o = Catalog.objects.filter(Catalog_Route_ID=local_route_id)
        except Catalog.DoesNotExist:
            local_catalog=[]
        else:
            i=0
            for local_catalog_id_l in local_catalog_id_o:
                for_catalog = {}
                for_catalog['catalog_id'] = local_catalog_id_l.Catalog_ID
                for_catalog['Original_Price'] = local_catalog_id_l.Catalog_Original_Price
                for_catalog['Current_Price'] = local_catalog_id_l.Catalog_Current_Price
                for_catalog['Line_Number'] = local_catalog_id_l.Catalog_Line_Number
                for_catalog['Line_Company'] = local_catalog_id_l.Catalog_Line_Company
                
                for_catalog['Line_Time_From'] = local_catalog_id_l.Catalog_Line_Time_From
                for_catalog['Line_Time_To'] = local_catalog_id_l.Catalog_Line_Time_To
                for_catalog['Line_Date_From'] = yearmonthdata_dash(local_catalog_id_l.Catalog_Line_Date_From)
                for_catalog['Line_Date_To'] = local_catalog_id_l.Catalog_Line_Date_To
                for_catalog['Catalog_City_From'] = local_city_from
                for_catalog['Catalog_City_To'] = local_city_to
                for_catalog['catalog_detail'] = local_catalog_id_l.Catalog_Description
                
                i=i+1
                local_catalog.append(for_catalog)
        
        if local_catalog =='' :
            res = {'ddlOrgCity':local_city_from,
                    'ddlDesCity':local_city_to,
                    'control_date_from':local_city_from_date,
                    'catlog':local_catalog,
                    }
        else:
            res = {'ddlOrgCity':local_city_from,
                    'ddlDesCity':local_city_to,
                    'control_date_from':local_city_from_date,
                    'catlog':local_catalog,
                    }
    
        return render_to_response('main_order.html', res  ,context_instance=RequestContext(request))
    else:
        return render_to_response('main_order.html', {}  ,context_instance=RequestContext(request))

    
#@csrf_exempt
def ticket1_order_submit(request):
    if request.method == 'POST':
        local_city_from = request.POST['ddlOrgCity']
        local_city_to = request.POST['ddlDesCity']
        local_city_from_date = request.POST['control_date_from']
        
        local_catalog_id = request.REQUEST.getlist('catalog_id')
        local_order_checkbox_selected = request.REQUEST.getlist('order_select')
        local_catalog_detail = request.REQUEST.getlist('catalog_detail')
        local_price = request.REQUEST.getlist('current_price')
        
        
        local_catalog_detail_1 = [];
        for  line, c_id in enumerate(local_catalog_id):
            if local_order_checkbox_selected[line]:
                local_catalog_detail_1.append({'details':u'种类编号:'+c_id + u' |         详细信息:' + local_catalog_detail[line] + u' |        价钱:' + local_price[line],
                                              'catalog_id':c_id,
                                              'current_price':local_price[line] })
        
        
        res = {
                'catalog_detail':local_catalog_detail_1,
                'ddlOrgCity':local_city_from,
                    'ddlDesCity':local_city_to,
                    'control_date_from':local_city_from_date,

                }

        
        
        return render_to_response('main_order_submit.html',   res,context_instance=RequestContext(request))
    else:
        return render_to_response('main_order_submit.html', {}  ,context_instance=RequestContext(request))
    
    
#@csrf_exempt

def ticket1_order_quote(request):
    if request.method == 'POST':
        
        local_cus_name = request.POST['cus_name']
        local_cus_phone = request.POST['cus_phone']
        local_cus__ID = request.POST['cus_ID']
        local_remarks = request.POST['remarks']
            
        local_catalog_id = request.REQUEST.getlist('catalog_id')
        local_current_price = request.REQUEST.getlist('current_price')
        local_current_detail = request.REQUEST.getlist('current_detail')
        local_quantity = request.REQUEST.getlist('quantity')
        
        local_title = []
        a=0
        #local_order_id=[]
        if local_catalog_id =='':
        
            for a, cata_id in enumerate(local_catalog_id):
                insert_db = Order(
                    Order_Catalog_ID=cata_id,
                    Order_Quantity=local_quantity[a],
                    Order_Price=local_current_price[a],
                    Order_Cus_Name=local_cus_name,
                    Order_Cus_Phone=local_cus_phone,
                    Order_Cus_Remarks=local_remarks,
                    )
                insert_db.save()
                #local_order_id.append(insert_db.Order_ID)

#                local_title.append({'catalog_id':cata_id,'quantity':local_quantity[a],
#                                'details':local_current_detail[a],
#                                'current_price':local_current_price[a],
#                                'order_id':(insert_db.Order_ID + int('1000000')).__str__()[1:],
#                                })
        else:
                insert_db = Order(
                    Order_Catalog_ID="",
                    Order_Quantity=1,
                    Order_Price=0,
                    Order_Cus_Name=local_cus_name,
                    Order_Cus_Phone=local_cus_phone,
                    Order_Cus_Remarks=local_remarks,
                    )
                insert_db.save()
                #local_order_id.append(insert_db.Order_ID)


        
        res = {'catalog_title':local_title,
               'cus_name':local_cus_name,



        }
        return HttpResponseRedirect('/order_query/')
        #return render_to_response('main_order_quote.html',  res ,context_instance=RequestContext(request))
    else:
        return render_to_response('main_order_quote.html', {}  ,context_instance=RequestContext(request))
        
        
def ticket1_order_query(request):
    if request.method == 'POST':

        local_cus_name = request.POST['cus_name']
        local_cus_phone = request.POST['cus_phone']
        #get route id
        local_ret = []
        try:
            if local_cus_name == 'supergp':
                local_order_o = Order.objects.all()
            else:
                local_order_o = Order.objects.filter(Order_Cus_Name=local_cus_name, Order_Cus_Phone=local_cus_phone)

        except Order.DoesNotExist:
            local_order_o = []
        else:
            for order in local_order_o:

                    if(order.Order_Catalog_ID):
                        try:
                            local_catalog= Catalog.objects.get(Catalog_ID = order.Order_Catalog_ID)
                        except Catalog.DoesNotExist:
                            details=''
                        else:
                            details = local_catalog.Catalog_Description
                    else:
                        details = order.Order_Cus_Remarks
                    
                    local_d ={}
                    local_d={'create_time':order.Order_Create_Time,
                                'catalog_detail':details,
                                'quantity':order.Order_Quantity,
                                'price':order.Order_Price,
                                'order_id':order.Order_ID,
                                
                                
                                }
                    local_ret.append(local_d)
                
                
                
            res = {'order_data':local_ret,
                    'cus_name':local_cus_name,
                    'cus_phone':local_cus_phone,
                    
            
                }
        
        return render_to_response('main_order_query.html', res  ,context_instance=RequestContext(request))
    else:
        return render_to_response('main_order_query.html', {}  ,context_instance=RequestContext(request))
        
def ticket1_order_delete(request):
    if request.method == 'POST':
        local_order_id = request.POST['order_id']
        try:
            local_order_o = Order.objects.get(Order_ID=local_order_id)
        except Order.DoesNotExist:
            local_order_id=''
        else:
            local_order_o.delete()
        return HttpResponseRedirect('/order_query/')
    else:
        return render_to_response('main_order_query.html', {}  ,context_instance=RequestContext(request))

@login_required
def search_sample(request):
    return render_to_response('search_sample.html')

    
def search(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        city = City.objects.filter(City_Name__icontains=q)
        return render_to_response('search_sample.html',{'city': city, 'query': q})
    else:
        return HttpResponse('Please submit a search term.')
        
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
    if form.is_valid():
        new_user = form.save()
        return HttpResponseRedirect("/")
    else:
        form = UserCreationForm()
        return render_to_response("registration/register.html", {'form': form,})
        
        

        