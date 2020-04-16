from django.forms import ModelForm
from fenouil.models import Mail

class MailForm(ModelForm):
	class Meta:
		model = Mail
		fields = ['contenu']