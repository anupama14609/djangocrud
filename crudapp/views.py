from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from .forms import UserRecordsManagement
from .models import User
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.
def add_show(request):
    error = ""
    if request.method == 'POST':
        form = UserRecordsManagement(request.POST)
        try:
            if form.is_valid():
                    name = form.cleaned_data['name']
                    email = form.cleaned_data['email']
                    password = form.cleaned_data['password']
                    records = User(name=name, email=email, password=password)
                    records.save()   
        except:
            error = "something went wrong"

    form = UserRecordsManagement()
    paginated_records = User.objects.all().order_by('-timeStamp')
    records = Paginator(paginated_records.filter(publish=True),4)
    page= request.GET.get('page')
    try:
        records = records.page(page)   
    except PageNotAnInteger:
        records  = records.page(1)
    except EmptyPage:
        records  = records.page(records.num_pages)

    context = {
        'form':form,
        'records':records,
        
        }
        
    return render(request, 'crudapp/showadded.html',context)

def delete_record(request,id):
    if request.method == 'POST':
        record_id = User.objects.get(pk=id)
        record_id.delete()
        return HttpResponseRedirect('/')

def update_record(request,id):
    if request.method == 'POST':
        record_id = User.objects.get(pk=id)
        form = UserRecordsManagement(request.POST, instance=record_id)
        if form.is_valid():
            form.save()

    else:
        record_id = User.objects.get(pk=id)
        form = UserRecordsManagement(instance=record_id)
    
    context = {
        'form':form,
    }
    print(context)
    return render(request, 'crudapp/update.html', context)

def update_database(request):
     queryset = User.objects.all()
     for record in queryset:
          record.save()
     return HttpResponseRedirect('/')   

def download_record(request):
    template_path = 'crudapp/downloads/download.html'
    posts = User.objects.all()
    context = {'allPost':posts}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="ExportRecord.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(
       html, dest=response)
  
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response