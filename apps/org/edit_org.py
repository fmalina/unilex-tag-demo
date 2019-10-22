from django.shortcuts import render, get_object_or_404, redirect
from org.models import Org, OrgUser
from org.forms_org import OrgForm


def owner_required(view_func):
    """Checks that the user is logged in and owns the item.
    redirecting home if necessary.
    """
    def wrap(request, pk, **kwargs):
        if request.user.is_authenticated:
            org = get_object_or_404(Org, pk=pk)
            if not org.is_editable_by(request.user):
                return redirect('/')
            return view_func(request, org, **kwargs)
        request.session['org_pk'] = pk
        return redirect('account_signup')
    wrap.__doc__=view_func.__doc__
    wrap.__name__=view_func.__name__
    return wrap


def edit_new(request):
    form = OrgForm(request.POST or None)
    if form.is_valid():
        org = form.save(commit=False)
        org.save()
        org_user = OrgUser(user=request.user, org=org)
        org_user.save()
        return redirect(org)
    return render(request, 'org/edit_contact.html', {
        'location': False,
        'edit_form': form
        })


@owner_required
def edit_contact(request, org):
    form = OrgForm(request.POST or None, instance=org)
    if form.is_valid():
        form.save()
        return redirect(org)
    return render(request, 'org/edit_contact.html', {
        'location': org,
        'edit_form': form
        })
