# utils.py

from flask import current_app
from datetime import time, datetime, date
from datetime import datetime 
from fpdf import FPDF
import barcode
from barcode.writer import ImageWriter
from PyPDF2 import PdfMerger
from io import BytesIO
import os
from PIL import Image
from pystrich.datamatrix import DataMatrixEncoder

def allowed_image_files(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def generate_time_options():
    time_options = []
    for hour in range(24):
        for minute in range(0, 60, 5):
            formatted_time = time(hour, minute).strftime('%H:%M')
            time_options.append(formatted_time)
    return time_options


def calculate_discount(date):
    depart_date = datetime.strptime(date, '%Y-%m-%d')
    today = datetime.now()
    days_away = (depart_date - today).days

    if 80 <= days_away <= 90:
        return 25, days_away
    elif 60 <= days_away <= 79:
        return 15, days_away
    elif 45 <= days_away <= 59:
        return 10, days_away
    else:
        return 0, days_away
    
    
def calculate_refund_amount(booking):
    days_until_departure = get_days_until_departure(booking)

    if days_until_departure  < 30:
        return 0, 0   # 0%
    elif 30 <= days_until_departure  < 60:
        return booking.amount_paid * 0.6, 60   # 60% refund
    else:
        return booking.amount_paid, 100   # 100% refund
    

def pretty_time(unformatted_time, to_12_hour=True):
    if unformatted_time == None:
        return None
    if not isinstance(unformatted_time, (datetime, time)):
        unformatted_time = datetime.strptime(unformatted_time, "%H:%M:%S")
    
    # Format the time
    if to_12_hour:
        formatted_time = unformatted_time.strftime("%I:%M %p")
    else:
        formatted_time = unformatted_time.strftime("%H:%M")
    
    return formatted_time

def get_days_until_departure(booking):
    today = datetime.now().date()
    return (booking.depart_date - today).days

def get_static_files(*path_parts):
    return os.path.join(current_app.root_path, 'static', *path_parts)

def create_receipt(booking, listing):
    formatted_depart_date = booking.depart_date.strftime('%d-%m-%Y')
    formatted_booking_date = booking.booking_date.strftime('%d-%m-%Y')
    formatted_depart_time = pretty_time(listing.depart_time)
    formatted_arrival_time = pretty_time(listing.destination_time)

    os.makedirs('/tmp', exist_ok=True)
    
    pdf = FPDF()
    pdf.add_page()
    
    company_logo_path = get_static_files('core', 'logo.jpeg')
    pdf.image(company_logo_path, x=10, y=8, w=33)
    
    pdf.set_font("Arial", size=40, style='B')
    pdf.cell(200, 10, txt="Receipt", ln=True, align='C')
    pdf.set_xy(10, 45)
    
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Number of Seats: {booking.num_seats}", ln=True)
    pdf.cell(200, 10, txt=f"Seat Type: {booking.seat_type.capitalize()}", ln=True)
    pdf.cell(200, 10, txt=f"Departure Date: {formatted_depart_date}", ln=True)
    pdf.cell(200, 10, txt=f"Departure Location: {listing.depart_location}", ln=True)
    pdf.cell(200, 10, txt=f"Departure Time: {formatted_depart_time}", ln=True)
    pdf.cell(200, 10, txt=f"Destination Location: {listing.destination_location}", ln=True)
    pdf.cell(200, 10, txt=f"Arrival Time: {formatted_arrival_time}", ln=True)
    pdf.cell(200, 10, txt=f"Booking Date: {formatted_booking_date}", ln=True)
    
    if booking.seat_type.lower() == 'economy':
        cost = listing.economy_fair_cost
    elif booking.seat_type.lower() == 'business':
        cost = listing.business_fair_cost
    
    pdf.cell(200, 10, txt=f"Total Cost: £{cost}", ln=True)

    pdf.set_font("Arial", size=16, style='B')
    pdf.set_xy(10, 200)
    pdf.cell(200, 10, txt="Thanks for choosing Horizon Travels!", ln=True, align='C')
    
    output = BytesIO()
    pdf.output(output)
    output.seek(0)
    
    return output

def create_plane_ticket(booking, listing):
    merger = PdfMerger()
    temp_files = []

    os.makedirs('/tmp', exist_ok=True)

    for seat_num in range(booking.num_seats):
        seat_number = f"{seat_num + 1:02d}"
        ticket_number = f"{booking.id}{listing.id}{booking.user_id}0000001PASS000000{seat_number}"

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=30, style='B')
        
        pdf.cell(200, 10, txt="Boarding Pass", ln=True, align='C')

        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Seat Number: {seat_number}", ln=True)
        pdf.cell(200, 10, txt=f"Seat Type: {booking.seat_type.capitalize()}", ln=True)
        pdf.cell(200, 10, txt=f"Departure Date: {booking.depart_date.strftime('%d-%m-%Y')}", ln=True)
        pdf.cell(200, 10, txt=f"Departure Location: {listing.depart_location}", ln=True)
        pdf.cell(200, 10, txt=f"Departure Time: {pretty_time(listing.depart_time)}", ln=True)
        pdf.cell(200, 10, txt=f"Destination Location: {listing.destination_location}", ln=True)
        pdf.cell(200, 10, txt=f"Arrival Time: {pretty_time(listing.destination_time)}", ln=True)
        pdf.cell(200, 10, txt=f"Transport Type: {listing.transport_type}", ln=True)

        datamatrix_img = create_datamatrix(ticket_number)
        datamatrix_img_path = f"/tmp/datamatrix_{ticket_number}.png"
        datamatrix_img.save(datamatrix_img_path)
        temp_files.append(datamatrix_img_path)
        pdf.image(datamatrix_img_path, x=100, y=30, w=75)

        barcode_img = create_barcode(ticket_number)
        barcode_img_path = f"/tmp/barcode_{ticket_number}.png"
        barcode_img.save(barcode_img_path)
        temp_files.append(barcode_img_path)
        pdf.image(barcode_img_path, x=60, y=120, w=100)

        output = BytesIO()
        pdf.output(output)
        output.seek(0)

        merger.append(output)

    final_output = BytesIO()
    merger.write(final_output)
    final_output.seek(0)

    for file_path in temp_files:
        os.remove(file_path)

    return final_output

def create_datamatrix(data):
    encoder = DataMatrixEncoder(data)
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
        encoder.save(temp_file.name)
        temp_file.seek(0)
        img = Image.open(temp_file.name)
    return img

def create_barcode(data):
    CODE128 = barcode.get_barcode_class('code128')
    options = {
        'write_text': False
    }
    code = CODE128(data, writer=ImageWriter())
    buffer = BytesIO()
    code.write(buffer, options=options)
    buffer.seek(0)
    img = Image.open(buffer)
    return img