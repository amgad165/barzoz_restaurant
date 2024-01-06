from django.core.mail import send_mail


def mail(order,sender, items_lists,payment_type):
    message = f"Sehr geehrte/r {order.user_details.vorname}   {order.user_details.nachname} ,\n \
vielen Dank für Ihre Bestellung bei Bazroz! Wir freuen uns sehr, dass Sie sich für unsere Küche entschieden haben und möchten Ihnen die Bestellung bestätigen.\n\n \
Bestellübersicht: \n \
Bestellnummer: {order.id} \n\n \
Bestellte Gerichte: \n \
 {items_lists} \n \
Weitere Informationen: {order.user_details.um_hinweise} \n \
Zahlungsart: {payment_type} \n \
Gesamtbetrag: {order.get_total()}€ \n\n \
Lieferdetails : \n \
Adresse: {order.user_details.street_address} \n \
Lieferzeit: 40 min \n \
Wir bereiten Ihre Gerichte mit größter Sorgfalt und nach höchsten Qualitätsstandards zu, um sicherzustellen, dass Ihr kulinarisches Erlebnis bei uns unvergesslich wird. Sollten Sie spezielle Wünsche oder Anmerkungen zu Ihrer Bestellung haben, zögern Sie bitte nicht, uns unter bazroz.restaurant@gmail.com oder +43676xxxxxxxxx zu kontaktieren. \n \
Bitte bewahren Sie diese E-Mail als Bestätigung Ihrer Bestellung auf. Wir freuen uns darauf, Sie bald bei Bazroz zu begrüßen! \n \
Mit freundlichen Grüßen, \n \
Ihr Team von Bazroz \n \
+43676xxxxxxxxx \n \
bazroz.restaurant@gmail.com \
    "
    
    
    client_email = [order.user_details.email]

    send_mail('Deine Bestellung bei Bazroz', message, from_email=sender ,recipient_list=client_email, fail_silently=False)

    message= f"Bestellnummer: {order.id} \n \
Bestellte Gerichte: \n\
{items_lists} \n\
Weitere Informationen: {order.user_details.um_hinweise} \n \
Kunden-E-Mail: {order.user_details.email} \n \
Telefonnummer des Kunden : {order.user_details.telefon} \n \
Adresse: {order.user_details.street_address} \n \
Link zur Bestellverwaltung : {order.user_details.street_address} \n \
    "
    # send email to bazroz mail 
    send_mail('Order arrived', message, from_email=sender ,recipient_list=[sender], fail_silently=False)
