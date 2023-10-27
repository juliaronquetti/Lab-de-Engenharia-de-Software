from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.
#O django cria por padrao a base de login com usuario e podemos usar a foreign key para outras bases

User = get_user_model()

#Nome da base de perfil
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) #pega o user da base de usuario
    id_user = models.IntegerField() #será o id de cada usuário na tabela
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png') #Ira criar uma pasta com as fotos de perfil
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username