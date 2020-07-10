from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

class userCreateForm(UserCreationForm):

	model=get_user_model()

	fields=('username','password1','password2')


	

	
