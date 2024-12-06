from django.forms import ModelForm
from comptes.models import TiendaUser

class TiendaUserForm(ModelForm):
    class Meta:
        model = TiendaUser
        fields = ['username', 'firstname', 'lastname', 'email', 'image']
