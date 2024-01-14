from django.core.mail import send_mail
from django.utils.html import format_html
from django.conf import settings

def mail(order,sender, items_lists,payment_type):
    
    image_url = f"{settings.STATIC_ROOT}assets/img/Bazroz_Logo_schrift.png"


    message = format_html(
        f"Sehr geehrte/r {order.user_details.vorname} {order.user_details.nachname},<br><br>"
        f"vielen Dank für Ihre Bestellung bei Bazroz! Wir freuen uns sehr, dass Sie sich für unsere Küche entschieden haben und möchten Ihnen die Bestellung bestätigen.<br><br>"
        f"<strong>Bestellübersicht:</strong><br>"
        f"Bestellnummer: {order.id}<br><br>"
        f"<strong>Bestellte Gerichte:</strong><br>"
        f"{items_lists}<br><br>"
        f"<strong>Weitere Informationen:</strong>{order.user_details.um_hinweise}<br>"
        f"Zahlungsart: {payment_type}<br>"
        f"Gesamtbetrag: {order.get_total()}€<br><br>"
        f"<strong>Lieferdetails:</strong><br>"
        f"Adresse: {order.user_details.street_address}<br>"
        f"Lieferzeit: 40 min<br><br>"
        f"Wir bereiten Ihre Gerichte mit größter Sorgfalt und nach höchsten Qualitätsstandards zu, um sicherzustellen, dass Ihr kulinarisches Erlebnis bei uns unvergesslich wird. Sollten Sie spezielle Wünsche oder Anmerkungen zu Ihrer Bestellung haben, zögern Sie bitte nicht, uns unter <a href='mailto:bazroz.restaurant@gmail.com'>bazroz.restaurant@gmail.com</a> oder <a href='tel:+43 681/81888778<'>+43 681/81888778<</a> zu kontaktieren.<br><br>"
        f"Bitte bewahren Sie diese E-Mail als Bestätigung Ihrer Bestellung auf. Wir freuen uns darauf, Sie bald bei Bazroz zu begrüßen!<br><br>"
        f"Mit freundlichen Grüßen,<br>"
        f"Ihr Team von Bazroz<br>"
        f"<a href='tel:+43 681/81888778'>+43 681/81888778</a><br>"
        f"Hauptstraße 4, 2340 Mödling<br>"
        f"<a href='mailto:bazroz.restaurant@gmail.com'>bazroz.restaurant@gmail.com</a>"
        f"<br><br><img src='{image_url}' alt='Bazroz Image'>"
    )

    client_email = [order.user_details.email]

    send_mail(
        'Deine Bestellung bei Bazroz',
        message,
        from_email=sender,
        recipient_list=client_email,
        fail_silently=False,
        html_message=message
    )
    

    message = format_html(
        f"Bestellnummer: {order.id},<br><br>"
        f"<strong>Bestellte Gerichte:</strong> <br><br>"
        f"{items_lists} <br><br>"
        f"Kunden-E-Mail: {order.user_details.email}<br><br>"
        f"Telefonnummer des Kunden: {order.user_details.telefon} <br><br>"
        f"Adresse: {order.user_details.street_address}<br>"
        f"Weitere Informationen:{order.user_details.um_hinweise} <br><br>"

    )

    # Send email to bazroz mail
    send_mail(
        'Order arrived',
        message,
        from_email=sender,
        recipient_list=[sender],
        fail_silently=False,
        html_message=message
    )
