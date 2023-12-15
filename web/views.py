from django.contrib.auth import get_user_model, login, authenticate, logout
from django.core.paginator import Paginator
from django.db.models import Prefetch, Count, Max, Min
from django.db.models.functions import TruncDate
from django.shortcuts import render, redirect, get_object_or_404

from web.forms import RegistrationForm, AuthForm, ProjectForm, TaskForm, CommentForm, TaskFilterForm
from web.models import Project, Task, Comment

User = get_user_model()


def index(request):
    user = request.user
    if user.is_authenticated:
        projects_list = Project.objects.filter(owner=user)
        return render(request, "web/main.html", {'projects': projects_list})
    else:
        return render(request, "web/main.html")


def register_view(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            login(request, user)
            return redirect('main')

    return render(request, 'web/registration.html', {'form': form})


def login_view(request):
    form = AuthForm()
    if request.method == 'POST':
        form = AuthForm(data=request.POST)
        if form.is_valid():
            user = authenticate(**form.cleaned_data)
            if user is not None:
                login(request, user)
                return redirect('main')
            else:
                form.add_error(None, 'Введены неверные данные')

    return render(request, 'web/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('main')


def project_detail(request, project_id):
    project = get_object_or_404(
        Project.objects.select_related('owner').annotate(total_comments=Count('tasks__comments')), pk=project_id)

    tasks = Task.objects.filter(project=project).prefetch_related(
        Prefetch('comments', queryset=Comment.objects.all().order_by('-date_added'))
    ).annotate(
        has_comments=Count('comments'),
    ).order_by('-creation_date')

    if request.method == 'GET':
        filter_form = TaskFilterForm(request.GET)
        if filter_form.is_valid():
            filters = filter_form.cleaned_data
            if filters['search']:
                tasks = tasks.filter(title__icontains=filters['search'])
            if filters['is_comment'] is not None:
                tasks = tasks.filter(has_comments__gt=0) if filters['is_comment'] else tasks.filter(has_comments=0)
    else:
        filter_form = TaskFilterForm()

    total_count = tasks.count()
    page_number = request.GET.get('page', 1)
    paginator = Paginator(tasks, per_page=5)

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            return redirect('project_detail', project_id=project_id)
    else:
        form = TaskForm()

    return render(request, 'web/project_detail.html', {'project': project,
                                                       'tasks': paginator.get_page(page_number), 'form': form,
                                                       'filter_form': filter_form, 'total_count': total_count})


def add_task(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user_assigned = request.user
            task.project = project
            task.save()
            return redirect('project_detail', project_id=project_id)
    else:
        form = TaskForm()

    return render(request, 'web/add_task.html', {'project': project, 'form': form})


def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            return redirect('project_detail', project_id=project.id)
    else:
        form = ProjectForm()

    return render(request, 'web/add_project.html', {'form': form})


def edit_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_detail', project_id=project_id)
    else:
        form = ProjectForm(instance=project)

    return render(request, 'web/edit_project.html', {'form': form, 'project': project})


def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    project.delete()
    return redirect('main')


def edit_task(request, project_id, task_id):
    project = get_object_or_404(Project, pk=project_id)
    task = get_object_or_404(Task, pk=task_id, project=project)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('project_detail', project_id=project_id)
    else:
        form = TaskForm(instance=task)

    return render(request, 'web/edit_task.html', {'form': form, 'project': project, 'task': task})


def delete_task(request, project_id, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.delete()
    return redirect('project_detail', project_id=project_id)


def add_comment(request, project_id, task_id):
    project = get_object_or_404(Project, pk=project_id)
    task = get_object_or_404(Task, pk=task_id, project=project)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.task = task
            comment.save()
            return redirect('project_detail', project_id=project_id)
    else:
        form = CommentForm()

    return render(request, 'web/add_comment.html', {'form': form, 'project': project, 'task': task})


def analytics_view(request):
    overall_statt = Task.objects.aggregate(
        count=Count("id"),
        max_date=Max("deadline"),
        min_date=Min("creation_date")
    )
    days_stat = (
        Task.objects.all()
        .annotate(date=TruncDate("deadline"))
        .values("date")
        .annotate(
            task_count=Count("id"),
            comment_count=Count("comments", distinct=True),
            start_date=Min("creation_date")
        )
    )
    return render(request, 'web/analytics.html', {
        'overall_statt': overall_statt,
        'days_stat': days_stat
    })