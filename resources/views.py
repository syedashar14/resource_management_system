from django.shortcuts import render, redirect
from .models import Resource, Project, Allocation
from .forms import ProjectForm, ResourceForm
from django.db.models import Sum

from django.db.models import Sum

def dashboard(request):
    allocations = Allocation.objects.select_related('resource', 'project')
    projects = Project.objects.all()

    resources = []
    total_allocations = []
    for allocation in allocations:
        resource = allocation.resource
        total_allocation_percentage = Allocation.objects.filter(resource=resource).aggregate(total=Sum('percentage_allocation'))['total']
        if total_allocation_percentage is not None:
            resources.append(resource)
            total_allocations.append(total_allocation_percentage)

    context = {
        'resources': zip(resources, total_allocations),
        'projects': projects,
        'allocations': allocations,
    }

    return render(request, 'resources/dashboard.html', context)




# def dashboard(request):
#     resources = Resource.objects.all()
#     projects = Project.objects.all()
#     allocations = Allocation.objects.select_related('resource', 'project')

#     context = {
#         'resources': resources,
#         'projects': projects,
#         'allocations': allocations,
#     }

#     return render(request, 'resources/dashboard.html', context)


def manage_allocations(request):
    resources = Resource.objects.all()
    projects = Project.objects.all()

    if request.method == 'POST':
        resource_id = request.POST.get('resource')
        project_id = request.POST.get('project')
        percentage_allocation = int(request.POST.get('percentage', 0))

        resource = Resource.objects.get(id=resource_id)
        project = Project.objects.get(id=project_id)

        total_allocation = Allocation.objects.filter(resource=resource, project=project).aggregate(total=Sum('percentage_allocation'))
        total_allocation_percentage = total_allocation['total'] or 0

        if total_allocation_percentage + percentage_allocation > 100:
            return render(request, 'resources/error.html', {'message': 'Total allocation percentage exceeds 100%'})

        allocation, created = Allocation.objects.get_or_create(resource=resource, project=project)
        allocation.percentage_allocation = percentage_allocation
        allocation.save()

        return redirect('resources:manage_allocations')

    allocations = Allocation.objects.select_related('resource', 'project')

    context = {
        'resources': resources,
        'projects': projects,
        'allocations': allocations,
    }

    return render(request, 'resources/manage_allocations.html', context)


def project_reports(request):
    projects = Project.objects.all()

    context = {
        'projects': projects,
    }

    return render(request, 'resources/project_reports.html', context)

def resource_reports(request):
    resources = Resource.objects.annotate(total_allocation=Sum('allocation__percentage_allocation'))

    context = {
        'resources': resources,
    }

    return render(request, 'resources/resource_reports.html', context)



def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('resources:dashboard')
    else:
        form = ProjectForm()
    
    return render(request, 'resources/add_project.html', {'form': form})

def add_resource(request):
    if request.method == 'POST':
        form = ResourceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('resources:dashboard')
    else:
        form = ResourceForm()
    
    return render(request, 'resources/add_resource.html', {'form': form})

def view_allocation(request, resource_id):
    resource = Resource.objects.get(id=resource_id)
    allocations = Allocation.objects.filter(resource=resource)
    total_allocation = allocations.aggregate(total=Sum('percentage_allocation'))['total']

    # Get the next resource
    next_resource = Resource.objects.filter(id__gt=resource_id).order_by('id').first()
    next_resource_id = next_resource.id if next_resource else None

    context = {
        'resource': resource,
        'allocations': allocations,
        'total_allocation': total_allocation,
        'next_resource_id': next_resource_id,
        'has_next_resource': bool(next_resource_id),  # Check if next_resource_id is not None
    }

    return render(request, 'resources/view_allocation.html', context)







def view_project_allocation(request, project_id):
    project = Project.objects.get(id=project_id)
    allocations = Allocation.objects.filter(project=project)

    context = {
        'project': project,
        'allocations': allocations,
    }

    return render(request, 'resources/view_project_allocation.html', context)

