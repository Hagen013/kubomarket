from django.core.mail import EmailMessage

from config.celery import app

NEW_ORDER_TEMPLATE = """
Уважаемый покупатель,
Ваш заказ с номером {number} поступил в обработку.
Мы свяжемся с Вами в ближайшее время для согласования.

С уважением,
kubomarket.ru
"""


@app.task
def client_new_order_notification(client_email, order_id):
    title = 'Ваш заказ с номером {number} поступил в обработку'.format(
        number=order_id,
    )
    text = NEW_ORDER_TEMPLATE.format(
        number=order_id,
    )
    email = EmailMessage(
        title,
        text,
        to=[client_email],
        reply_to=['info@kubomarket.ru'],
    )
    email.send()


@app.task
def anton_new_order_notification(order_id,
                                 client_phone,
                                 client_name,
                                 client_email,
                                 client_address,
                                 client_notes,
                                 delivery_code,
                                 delivery_mode,
                                 products=[]
                                 ):
    title = 'cubes_new_order|{number}'.format(
        number=order_id,
    )

    products_text = "-----------".join([
        """
        name={name},
        vendor_code:{vendor_code}
        price:{price}
        quantity:{quantity}
        """.format(
            name=p['name'],
            vendor_code=p['vendor_code'],
            quantity=p["quantity"],
            price=p['price']
        )
        for p in products
    ])

    text = """
    client_phone:{client_phone}
    client_name:{client_name}
    client_email:{client_email}
    client_address:{client_address}
    client_notes:{client_notes}
    products:
    {products_text}
    delivery_code:{delivery_code}
    delivery_node:{delivery_mode}
    """.format(
        client_phone=client_phone,
        client_name=client_name,
        client_email=client_email,
        client_address=client_address,
        client_notes=client_notes,
        products_text=products_text,
        delivery_code=delivery_code,
        delivery_mode=delivery_mode,
    )
    email = EmailMessage(
        title,
        text,
        to=['akontuzov@mail.ru'],
        reply_to=['info@kubomarket.ru'],
    )
    # print(text)
    email.send()
