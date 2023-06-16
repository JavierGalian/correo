from django.shortcuts import render, redirect
from .forms import NewsletterUserSignupForm
from .models import NewsletterUser
from django.contrib import messages as django_messages
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMultiAlternatives, EmailMessage
# Create your views here.
def newsletter_signup(request):
    if request.method == 'POST':
        form = NewsletterUserSignupForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            if NewsletterUser.objects.filter(email=instance.email).exists():
                django_messages.warning(request, 'Email ya existe')

            else:
                instance.save()
                django_messages.success(request, 'Hemos enviado un correo electrónico a tu correo')
                #correo electronico
                subject = "libro de cocina"
                from_email = settings.EMAIL_HOST_USER
                to_email = [instance.email] #a quien le estamos enviando este email

                html_template = 'newsletters/email_templates/welcome.html'
                html_message = render_to_string(html_template) #convierto  welcome.html en string
                message=EmailMessage(subject, html_message, from_email, to_email) #envio el email con los datos obtenidos
                message.content_subtype='html' #typo de mensaje que quiero enviar html es mas rapido
                message.send()
    else:
        form = NewsletterUserSignupForm()
    
    contexto={
        'form':form
    }
    return render(request, 'start-here.html', contexto)

#funcion para dessuscribirse
def newsletter_unsubscribe(request):
    form = NewsletterUserSignupForm(request.POST or None) #form obtiene un solo correo

    if form.is_valid():#si email existe en la base de datos
        instance = form.save(commit=False)
        if NewsletterUser.objects.filter(email=instance.email).exists():
            NewsletterUser.objects.filter(email=instance.email).delete()
            django_messages.success(request, 'correo electronico eliminado')
        else:
            print('email no encontrado')
            django_messages.warning(request, 'Email no existe')
    context = {
        'form':form
    }
    return render(request, 'unsubscribe.html', context)