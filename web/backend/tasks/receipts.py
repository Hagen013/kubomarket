from datetime import datetime
from weasyprint import HTML

from django.conf import settings
from django.template.loader import get_template

from cart.models import Order2


def generate_receipt(pk):
    template = get_template("receipt.html")
    instance = Order2.objects.get(id=pk)
    context = {
        "order": instance,
        "date": datetime.now().strftime("%d.%m.%Y")
    }
    html = template.render(context=context)
    output_filename = "{path}{public_id}.pdf".format(
        path=settings.RECEIPTS_PATH,
        public_id=instance.public_id
    )
    pdf_file = HTML(string=html).write_pdf(output_filename)
    return output_filename

