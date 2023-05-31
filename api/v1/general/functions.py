import base64

from django.core.files.base import ContentFile

from mailqueue.models import MailerMessage
from general.functions import generate_unique_id,randomnumber


"""
To get serializer errors from validation errors
"""
def generate_serializer_errors(args):
    message = ""
    for key, values in args.items():
        error_message = ""
        for value in values:
            error_message += value + ","
        error_message = error_message[:-1]

        message += f"{key} - {error_message} | "

    return message[:-3]


def send_email(to_address, subject, content, html_content, attachment=None, attachment2=None, attachment3=None, bcc_address=None):
    new_message = MailerMessage()
    new_message.subject = subject
    new_message.to_address = to_address
    if bcc_address:
        new_message.bcc_address = bcc_address
    new_message.from_address = "Socialwaves Pvt Ltd"
    new_message.content = content
    new_message.html_content = html_content
    if attachment:
        new_message.add_attachment(attachment)
    if attachment2:
        new_message.add_attachment(attachment2)
    if attachment3:
        new_message.add_attachment(attachment3)
    new_message.app = "default"
    new_message.save()

    return new_message.sent


# def generate_unique_username(username):

#     if User.objects.filter(username=username).exists():
#         username = generate_unique_id(20)

#         generate_unique_username(username)

#     return username


def convert_base64_image_to_image(base64_image:str,name:str=None):
    """
         converting base64 image into normal image type
    """
    format, imgstr = base64_image.split(';base64,')
    ext = format.split('/')[-1]

    if not name:
        name = randomnumber(20)

    final_image = ContentFile(base64.b64decode(imgstr), name=f'{name}.{ext}')

    return final_image