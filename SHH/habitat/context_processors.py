from .forms import UserForm

# https://stackoverflow.com/questions/17901341/django-how-to-make-a-variable-available-to-all-templates
def user_form_processor(request):
    user_form = UserForm()
    return {'user_form': user_form}