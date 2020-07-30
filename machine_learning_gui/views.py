from django.views.generic import TemplateView

class ThankYou(TemplateView):

	template_name = 'thanks.html'


class Welcome(TemplateView):

	template_name='welcome.html'



class HomePage(TemplateView):
	template_name = 'home.html'
	