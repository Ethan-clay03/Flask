# utils.py

from flask import current_app
from datetime import time, datetime
from datetime import datetime 
from fpdf import FPDF
import qrcode
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
import os
from PIL import Image

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
    

def pretty_time(unformatted_time, to_12_hour=True):
    if not isinstance(unformatted_time, (datetime, time)):
        unformatted_time = datetime.strptime(unformatted_time, "%H:%M:%S")
    
    # Format the time
    if to_12_hour:
        formatted_time = unformatted_time.strftime("%I:%M %p")
    else:
        formatted_time = unformatted_time.strftime("%H:%M")
    
    return formatted_time



def get_static_files(*path_parts):
    return os.path.join(current_app.root_path, 'static', *path_parts)

def create_receipt(seat_num, seat_type, depart_date, listing):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Add company logo
    company_logo_path = get_static_files('core', '1.jpg')
    pdf.image(company_logo_path, x=10, y=8, w=33)
    
    # Adjust y position to avoid overlapping
    pdf.set_xy(10, 45)
    pdf.cell(200, 10, txt="Receipt", ln=True, align='C')
    
    pdf.cell(200, 10, txt=f"Seat Number: {seat_num}", ln=True)
    pdf.cell(200, 10, txt=f"Seat Type: {seat_type}", ln=True)
    pdf.cell(200, 10, txt=f"Departure Date: {depart_date}", ln=True)
    pdf.cell(200, 10, txt=f"Departure Location: {listing.depart_location}", ln=True)
    pdf.cell(200, 10, txt=f"Destination Location: {listing.destination_location}", ln=True)
    
    if seat_type.lower() == 'economy':
        cost = listing.economy_fair_cost
    elif seat_type.lower() == 'business':
        cost = listing.business_fair_cost
    
    pdf.cell(200, 10, txt=f"Total Cost: {cost}", ln=True)
    
    # Generate barcode
    receipt_data = f"{seat_num},{seat_type},{depart_date},{listing.depart_location},{listing.destination_location},{cost}"
    code128 = barcode.get('code128', receipt_data, writer=ImageWriter())
    barcode_image = BytesIO()
    code128.write(barcode_image)
    barcode_image.seek(0)
    
    # Save barcode image
    with open("barcode.png", "wb") as f:
        f.write(barcode_image.read())
    
    pdf.image("barcode.png", x=150, y=8, w=50)
    
    # Add thank you message
    pdf.set_font("Arial", size=16, style='B')
    pdf.set_xy(10, 250)
    pdf.cell(200, 10, txt="Thanks for choosing Horizon Travels!", ln=True, align='C')
    
    output = BytesIO()
    pdf.output(output)
    output.seek(0)
    
    return output


def create_plane_ticket(seat_num, seat_type, depart_date, listing, booking_id):
    for i in range(seat_num):
        seat_number = f"{seat_num + 1 - i:02d}"
        ticket_number = f"{booking_id}-{seat_number}"

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        pdf.cell(200, 10, txt="Plane Ticket", ln=True, align='C')

        pdf.cell(200, 10, txt=f"Seat Number: {seat_number}", ln=True)
        pdf.cell(200, 10, txt=f"Seat Type: {seat_type}", ln=True)
        pdf.cell(200, 10, txt=f"Departure Date: {depart_date}", ln=True)
        pdf.cell(200, 10, txt=f"Departure Location: {listing.depart_location}", ln=True)
        pdf.cell(200, 10, txt=f"Departure Time: {listing.depart_time}", ln=True)
        pdf.cell(200, 10, txt=f"Destination Location: {listing.destination_location}", ln=True)
        pdf.cell(200, 10, txt=f"Destination Time: {listing.destination_time}", ln=True)
        pdf.cell(200, 10, txt=f"Transport Type: {listing.transport_type}", ln=True)

        qr_img = create_qr_code(ticket_number)
        qr_img_path = f"qr_code_{ticket_number}.png"
        qr_img.save(qr_img_path)
        pdf.image(qr_img_path, x=10, y=120, w=50)

        barcode_img = create_barcode(ticket_number)
        barcode_img_path = f"barcode_{ticket_number}.png"
        barcode_img.save(barcode_img_path)
        pdf.image(barcode_img_path, x=80, y=120, w=100)

        output = BytesIO()
        pdf.output(output)
        output.seek(0)

        return output

def create_qr_code(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    return img

def create_barcode(data):
    CODE128 = barcode.get_barcode_class('code128')
    code = CODE128(data, writer=ImageWriter())
    buffer = BytesIO()
    code.write(buffer)
    return Image.open(buffer)