from django.contrib.auth import get_user_model

User = get_user_model()

username = "Matematico"
email = "Mat@gmail.com"
password = "123456789"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print("Superuser criado com sucesso!")
else:
    print("Superuser já existe.")