from django.shortcuts import render
from shop.models import Profile  # Importa los modelos necesarios
from django.shortcuts import render, get_object_or_404

def profile_list(request):
    profiles = Profile.objects.all()
    return render(request, 'profile_list.html', {'profiles': profiles})

def profile_detail(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    return render(request, 'admin_panel/profile_detail.html', {'profile': profile})