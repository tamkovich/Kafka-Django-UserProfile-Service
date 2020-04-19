from django.views import generic


class LoginView(generic.TemplateView):
    template_name = 'login.html'


class ProduceUser(generic.View):
    def post(self, request, *args, **kwargs):
        import pdb; pdb.set_trace()


class SwitchBoardView(generic.View):
    def get(self, request, *args, **kwargs):
        view = LoginView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = ProduceUser.as_view()
        return view(request, *args, **kwargs)
