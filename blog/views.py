from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, CreateView, ListView, UpdateView, DeleteView, TemplateView

from blog.forms import BlogForm
from blog.models import Blog
from blog.services import get_mails_from_cache, get_clients_from_cache


class BlogListView(ListView):
    model = Blog
    context_object_name = 'posts'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        for post in context['posts']:
            post.content = post.content[:25]
        return context

    def get_queryset(self):
        return Blog.objects.filter(is_active=True).order_by('-views')


class BlogDetailView(DetailView):
    model = Blog
    context_object_name = 'post'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views += 1
        self.object.save()
        return self.object


class BlogCreateView(CreateView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('blog:blog_list')


class BlogUpdateView(UpdateView):
    model = Blog
    form_class = BlogForm

    def get_success_url(self):
        return reverse('blog:blog_detail', args=[self.kwargs.get('pk')])


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:blog_list')


class HomePageView(TemplateView):
    template_name = 'blog/home_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        mails_list = get_mails_from_cache()
        clients_list = get_clients_from_cache()

        total_mailings = mails_list.count()
        active_mailings = mails_list.filter(is_active=True).count()
        unique_clients = clients_list.count()
        last_blogs = Blog.objects.filter(is_active=True)[:3]

        context['total_mailings'] = total_mailings
        context['active_mailings'] = active_mailings
        context['unique_clients'] = unique_clients
        context['last_blogs'] = last_blogs

        return context
