from django.shortcuts import render, redirect, get_object_or_404
from .models import Blog
from .forms import BlogForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .models import UserProfile
from django.contrib.auth.views import LogoutView


def homePage(request):
    latest_blogs = Blog.objects.all().order_by('-created_at')[:3]
    return render(request, 'home.html', {'latest_blogs': latest_blogs})

class CustomLoginView(LoginView):
   def get_success_url(self):
    try:
        profile = self.request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=self.request.user)
        
        if profile.user_profiles.exists():
            user_id = profile.user_profiles.first().id
            return reverse_lazy('muscian_restricted', kwargs={'user_id': user_id})
        
        return reverse_lazy('Restricted_page')

class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
    
@login_required
def restricted_page(request):
    data = {
        'title': 'Restricted Page',
        'content': '<h1>You are logged in</h1>'
    }
    return render(request, "general.html", data)
    


@login_required
def user_restricted(request, user_id):
    try:
        user = get_object_or_404(Blog, id=user_id)
        profile = request.user.userprofile
        allowed = False
        
        if profile.user_profile.filter(id=user.id).exists():
            allowed = True
        else:
            userprofiles = set(profile.user_profile.all())
            for users in user.all():
                user_blogs = set(users.user.all())
                if userprofiles.intersection(user_blogs):
                    allowed = True
                    break
        
        if not allowed:
            return redirect('Restricted_page') 
        
        content = f"""
        <h1>Blog title: {user.title}</h1>
        <p>Blog content: {user.content}</p>
        """
        data = {
            'title': 'Restricted Musician Page',
            'content': content,
        }
        return render(request, "general.html", data)
    
    except Exception as e:
        return redirect('Restricted_page')  
    

def blog_list(request):
    blogs = Blog.objects.all().order_by('-created_at')
    return render(request, 'blog_list.html', {'blogs': blogs})

@login_required
def blog_create(request):
    form = BlogForm(request.POST or None)
    if form.is_valid():
        blog = form.save(commit=False)
        blog.author = request.user
        blog.save()
        return redirect('blog_list')
    return render(request, 'blog_form.html', {'form': form})

@login_required
def blog_edit(request, pk):
    blog = get_object_or_404(Blog, pk=pk, author=request.user)
    form = BlogForm(request.POST or None, instance=blog)
    if form.is_valid():
        form.save()
        return redirect('blog_list')
    return render(request, 'blog_form.html', {'form': form})

@login_required
def blog_delete(request, pk):
    blog = get_object_or_404(Blog, pk=pk, author=request.user)
    if request.method == 'POST':
        blog.delete()
        return redirect('blog_list')
    return render(request, 'blog_confirm_delete.html', {'blog': blog})
