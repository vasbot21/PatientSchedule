from django.shortcuts import render, redirect
from .models import *
from .forms import PatientForm
from datetime import datetime


def patients(request):
    context = {'patients': {}, 'number': len(Patient.objects.all())}
    for patient in Patient.objects.all().order_by('surname', 'name', 'patronymic'):
        context['patients'][str(patient.id)] = {}
        context['patients'][str(patient.id)]['patient'] = patient.__str__()
        context['patients'][str(patient.id)]['id'] = patient.id
        context['patients'][str(patient.id)]['surname'] = patient.surname
        context['patients'][str(patient.id)]['name'] = patient.name
        if patient.patronymic:
            context['patients'][str(patient.id)]['patronymic'] = patient.patronymic
        else:
            context['patients'][str(patient.id)]['patronymic'] = ''
        context['patients'][str(patient.id)]['phone'] = patient.format_phone()
        if patient.birth_year:
            context['patients'][str(patient.id)]['birth_year'] = patient.birth_year
        else:
            context['patients'][str(patient.id)]['birth_year'] = ''
        if patient.black_list:
            context['patients'][str(patient.id)]['black_list'] = '1'
        else:
            context['patients'][str(patient.id)]['black_list'] = '0'
    return render(request, 'PatientSchedule/patients.html', context)


def format_birth_year(request):
    birth_year = request.POST.get('birth_year')
    if len(birth_year) == 1:
        birth_year = '200' + birth_year
    elif (len(birth_year) == 2) and (birth_year >= '0') and ('20' + birth_year <= str(datetime.now().year)):
        birth_year = '20' + birth_year
    else:
        birth_year = '19' + birth_year
    return birth_year


def add_patient(request):
    if request.method == 'POST':
        if not Patient.objects.filter(surname=request.POST.get('surname'), name=request.POST.get('name'),
                                      phone=request.POST.get('phone')):
            form = PatientForm(request.POST)
            if form.is_valid():
                form.save()
        form = PatientForm(label_suffix='')
    else:
        form = PatientForm(label_suffix='')
    return render(request, 'PatientSchedule/add_patient.html', {'form': form})


def patient(request, patient_id):
    if request.method == 'POST':
        Patient.objects.filter(pk=patient_id).update(surname=request.POST.get('surname'),
                                                     name=request.POST.get('name'),
                                                     phone=request.POST.get('phone'))
        if request.POST.get('birth_year'):
            Patient.objects.filter(pk=patient_id).update(birth_year=format_birth_year(request))
        if request.POST.get('patronymic'):
            Patient.objects.filter(pk=patient_id).update(patronymic=request.POST.get('patronymic'))
        if request.POST.get('black_list'):
            Patient.objects.filter(pk=patient_id).update(black_list=True)
        else:
            Patient.objects.filter(pk=patient_id).update(black_list=False)
        if request.POST.get('text'):
            Patient.objects.filter(pk=patient_id).update(text=request.POST.get('text'))
    patient = Patient.objects.get(pk=patient_id)
    context = {
        'id': patient.id,
        'surname': patient.surname,
        'name': patient.name,
        'phone': patient.phone
    }
    if patient.birth_year:
        context['birth_year'] = patient.birth_year
    if patient.patronymic:
        context['patronymic'] = patient.patronymic
    if patient.black_list:
        context['black_list'] = patient.black_list
    if patient.text:
        context['text'] = patient.text
    return render(request, 'PatientSchedule/patient.html', context)


def delete_patient(request, patient_id):
    patient = Patient.objects.get(pk=patient_id)
    patient.delete()
    return redirect('patients')
