from django.shortcuts import render, get_object_or_404, redirect
from org.models import Org
from upload.models import File
from django_messages.forms import ComposeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse


def detail(request, pk=0, slug=0):
    org = get_object_or_404(Org, pk=pk)

    # redirect outdated slugs to new
    if request.path_info != org.get_absolute_url():
        return redirect(org.get_absolute_url(), permanent=True)

    photos = File.objects.filter(col=org)
    org_user = org.orguser_set.first()

    return render(request, 'org/detail.html', {
        'o': org,
        'org_user': org_user,
        'photos': photos
    })


@login_required
def compose(request, recipient):
    if request.method == "POST":
        print(request.POST)
        form = ComposeForm(request.POST)
        if form.is_valid():
            form.save(sender=request.user)
            messages.info(request, "Message successfully sent.")
            success_url = reverse('profile')
            if 'next' in request.GET:
                success_url = request.GET['next']
            return redirect(success_url)
    else:
        form = ComposeForm()
        if recipient is not None:
            recipients = [u for u in User.objects.filter(**{
                'username__in': [r.strip() for r in recipient.split('+')]
            })]
            form.fields['recipient'].initial = recipients
    return render(request, 'django_messages/compose.html', {
        'form': form,
    })


def after_joining(request):
    pk = request.session.get('org_pk')
    if pk:
        org = Org.objects.get(pk=pk)
        return redirect(org.get_edit_url())
    return redirect('/profile')
