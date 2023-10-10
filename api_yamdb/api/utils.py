from django.core.mail import send_mail


def send_confirmation_code(email, confirmation_code):
    """Отправляет код подтверждения на почту пользователю."""
    send_mail(
        subject='Код подтверждения',
        message=f'Ваш код подтверждения: {confirmation_code}',
        from_email='registration_YAMDB@mail.com',
        recipient_list=(email,),
        fail_silently=False,
    )
