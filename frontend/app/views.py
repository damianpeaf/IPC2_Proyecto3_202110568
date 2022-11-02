from django.shortcuts import render
from requests import post, get
from .forms import ConfigurationMessageForm,ClientForm,InstanceForm, BillForm,ConsumptionMessageForm, ResourceForm

def index(request):
    return render(request, 'index.html')


def reset(request):
    post('http://localhost:5000/resetear')
    return render(request, 'reset.html')

def configuration(request):

    if request.method == 'POST':
        form = ConfigurationMessageForm(request.POST, request.FILES)

        if form.is_valid():
            resp = post('http://localhost:5000/mensajeConfiguracion', files=request.FILES)
            msgs = resp.json()['msgs']
            return render(request, 'configuration.html', {'form': form, 'msgs':msgs})
    else:
        form = ConfigurationMessageForm()

    return render(request, 'configuration.html', {'form': form, 'msgs':[]})

def consumption(request):

    if request.method == 'POST':
        form = ConsumptionMessageForm(request.POST, request.FILES)

        if form.is_valid():
            resp = post('http://localhost:5000/mensajeConsumo', files=request.FILES)
            msg = resp.json()['msg']
            print(resp.json())
            return render(request, 'consumption.html', {'form': form, 'msg':msg})
    else:
        form = ConsumptionMessageForm()

    return render(request, 'consumption.html', {'form':form,'msg':''})

def about(request):
    return render(request, 'about.html')

def operation(request):
    return render(request, 'operations.html')

def consult(request):

    resp = get('http://localhost:5000/consultarDatos')
    data =  resp.json()

    # print(data['categories'])
    return render(request, 'consult.html', {'data':data})

def create(request):
    return render(request, 'create.html')

def bill(request):
    return render(request, 'bill.html')

def report(request):
    return render(request, 'report.html')

def create_resource(request):
    if request.method == 'POST':
        form = ResourceForm(request.POST)

        if form.is_valid():
            resp = post('http://localhost:5000/crearRecurso', json=request.POST)
            msg = resp.json()['msg']
            return render(request, 'creation.html', {'form': form, 'msg':msg})
    else:
        form = ResourceForm()

    return render(request, 'creation.html', {'form':form,'msg':''})

def create_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)

        if form.is_valid():
            resp = post('http://localhost:5000/crearCliente', json=request.POST)
            msg = resp.json()['msg']
            return render(request, 'creation.html', {'form': form, 'msg':msg})
    else:
        form = ClientForm()

    return render(request, 'creation.html', {'form':form,'msg':''})

def create_instance(request):
    if request.method == 'POST':
        form = InstanceForm(request.POST)

        if form.is_valid():
            resp = post('http://localhost:5000/crearInstancia', json=request.POST)
            msg = resp.json()['msg']
            return render(request, 'creation.html', {'form': form, 'msg':msg})
    else:
        form = InstanceForm()

    return render(request, 'creation.html', {'form':form,'msg':''})

def create_bill(request):
    if request.method == 'POST':
        form = BillForm(request.POST)

        if form.is_valid():
            data = request.POST
            resp = post('http://localhost:5000/generarFactura', json=data)
            msg = resp.json()['msg']
            return render(request, 'creation.html', {'form': form, 'msg':msg})
    else:
        form = BillForm()

    return render(request, 'creation.html', {'form':form,'msg':''})