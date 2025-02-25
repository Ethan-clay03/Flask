from flask import render_template, redirect, url_for, request, jsonify, session, flash, g, send_file
from flask_login import current_user
from app.bookings import bp
from app.models import Listings, Bookings, ListingAvailability
from app import db
from app.logger import error_logger
from app.main.utils import calculate_discount, pretty_time, create_receipt, create_plane_ticket, calculate_refund_amount
import json
from datetime import datetime
from app import user_permission, permission_required


@bp.route('/')
def redirect_index():
    return redirect(url_for('bookings.listings'), code=301)

@bp.route('/listings')
def listings():
    depart_location = request.args.get('departLocation')
    destination_location = request.args.get('destinationLocation')
    depart_date = request.args.get('departDate')
    seat_type = request.args.get('seatType', 'economy')

    page = request.args.get('page', 1, type=int)
    per_page = 10

    # Calculate discount based on departure date
    discount, days_away = calculate_discount(depart_date) if depart_date else (0, 0)

    all_listings = Listings.get_all_listings()

    if depart_location:
        all_listings = [listing for listing in all_listings if listing.depart_location == depart_location]
    if destination_location:
        all_listings = [listing for listing in all_listings if listing.destination_location == destination_location]

    # Calculate total cost and apply discount, also change time to nicer format
    for listing in all_listings:
        if seat_type == 'economy':
            listing.discounted_cost = listing.economy_fair_cost * (1 - discount / 100)
            listing.original_cost = listing.economy_fair_cost
        elif seat_type == 'business':
            listing.discounted_cost = listing.business_fair_cost * (1 - discount / 100)
            listing.original_cost = listing.business_fair_cost

    # Calculate pagination items and how many listings exist
    total_items = len(all_listings)
    paginated_listings = all_listings[(page - 1) * per_page: page * per_page]

    process_images(paginated_listings)

    # Get all locations for dropdowns
    locations = Listings.get_all_locations(True)

    return render_template(
        'bookings/listings.html',
        items=paginated_listings,
        page=page,
        total_pages=(total_items + per_page - 1) // per_page,
        locations=locations,
        discount=discount,
        days_away=days_away,
        depart_date=depart_date,
        form_data={
            'departLocation': depart_location,
            'destinationLocation': destination_location,
            'seatType': seat_type
        }
    )
@bp.route('/listing/apply_update', methods=['POST'])
def listing_apply_update(): 
    data = request.get_json()
    selected_date = data.get('date')
    num_seats = int(data.get('seats'))
    seat_type = data.get('seatType')
    
    discount, days_away = calculate_discount(selected_date)

    listing = session['listing']
    if seat_type == "business":
        base_price = listing['business_fair_cost']
    else:
        base_price = listing['economy_fair_cost']
    
    discounted_price = base_price * (1 - discount / 100)
    total_cost = discounted_price * num_seats
    total_saved = (base_price * num_seats) - total_cost

    response = {
        'discount': discount,
        'days_away': days_away,
        'base_price': base_price,
        'discounted_price': discounted_price,
        'total_cost': total_cost,
        'total_saved': total_saved
    }
    return jsonify(response)


@bp.route('/checkout')
@permission_required(user_permission)
def checkout():
    if not session.get('checkout_cache'):
        flash("Please select a booking", 'error')
        return redirect(url_for('bookings.listings'))

    cache = session['checkout_cache']
    depart_date = cache['depart_date']
    num_seats = int(cache['num_seats'])
    listing_id = cache['listing_id']
    seat_type = cache['seat_type']

    listing = Listings.search_listing(listing_id)
    listing.depart_time = pretty_time(listing.depart_time)
    listing.destination_time = pretty_time(listing.destination_time)

    per_person_excluding_discount = listing.business_fair_cost if seat_type == 'business' else listing.economy_fair_cost
    discount_percentage, days_away = calculate_discount(depart_date)
    
    discount_amount = (per_person_excluding_discount * discount_percentage) / 100
    per_person_cost = per_person_excluding_discount - discount_amount

    listing.per_person_cost = per_person_cost
    listing.total_cost = per_person_cost * num_seats
    total_savings = discount_amount * num_seats

    # Add per_person_cost to checkout_cache in session
    session['checkout_cache']['per_person_cost'] = per_person_cost

    depart_date_obj = datetime.strptime(depart_date, '%Y-%m-%d')
    depart_date_formatted = depart_date_obj.strftime('%d-%m-%Y')

    return render_template(
        'bookings/checkout.html', 
        listing=listing, 
        num_seats=num_seats, 
        depart_date=depart_date_formatted, 
        seat_type=seat_type.capitalize(), 
        total_savings=total_savings
    )


@bp.route('/payment')
@permission_required(user_permission)
def payment(): 
    depart_date = request.args.get('date')
    num_seats = request.args.get('seats')
    listing_id = request.args.get('listing_id')
    seat_type = request.args.get('seat_type')

    if not depart_date or not num_seats or not listing_id or not seat_type:
        flash('Please select a booking in order to checkout.', 'error')
        return redirect(url_for('bookings.listings'))

    session['checkout_cache'] = {
        'listing_id': listing_id,
        'depart_date': depart_date,
        'num_seats': num_seats,
        'listing_id': listing_id,
        'seat_type': seat_type
    }

    return redirect(url_for('bookings.checkout'))

@bp.route('/show_listing/<int:id>', methods=['GET'])
def show_listing_dirty(id):
    # Retrieve query parameters
    session['filter_data'] = request.args.to_dict()

    return redirect(url_for('bookings.listing', id=id))

# This route should be used after show_listing if used internally as this clears the ajax parameters before redirecting the user
@bp.route('/listing/<int:id>', methods=['GET'])
def listing(id):
    listing = Listings.search_listing(id)
    
    if 'listing' not in session:
        session['listing'] = {}

    session['listing']['economy_fair_cost'] = listing.economy_fair_cost
    session['listing']['business_fair_cost'] = listing.business_fair_cost

    depart_time = pretty_time(listing.depart_time)
    destination_time = pretty_time(listing.destination_time)
    filter_data = session.pop('filter_data', None)

    selected_date = filter_data['date'] if filter_data and 'date' in filter_data else None
    seat_type = filter_data['seatType'] if filter_data and 'seatType' in filter_data else 'economy'

    discount, days_away = calculate_discount(selected_date) if selected_date else (0, 0)

    if seat_type == "business":
        base_price = listing.business_fair_cost
    else:
        base_price = listing.economy_fair_cost

    main_image_url = 'booking_image_not_found.jpg'
    for image in listing.listing_images:
        if image.main_image == 1:
            main_image_url = image.image_location
            break


    discounted_price = base_price * (1 - discount / 100)
    total_cost = discounted_price

    return render_template(
        'bookings/listing.html',
        listing=listing,
        selected_date=selected_date,
        seat_type=seat_type,
        discount=discount,
        days_away=days_away,
        base_price=base_price,
        discounted_price=discounted_price,
        total_cost=total_cost,
        depart_time = depart_time, 
        destination_time = destination_time,
        main_image_url = main_image_url
    )

# This route should be used after show_listing if used internally as this clears the ajax parameters before redirecting the user
@bp.route('/checkout/success/<int:id>', methods=['GET'])
@permission_required(user_permission)
def payment_complete(id):
    
    booking = Bookings.search_booking(id)

    if booking.user_id != g.identity.id:
        flash ("Unable to load payment, please check your booking ID", 'error')
        return redirect(url_for('main.index'))

    return render_template(
        'bookings/payment_success.html', id=booking.id
    )

@bp.route('/checkout_post', methods=['POST'])
@permission_required(user_permission)
def checkout_post():
    card_number = request.form['cardNumber']
    card_expiry = request.form['cardExpiry']
    card_cvc = request.form['cardCVC']
    
    valid_payment_details, payment_error_message = validate_payment(card_number, card_expiry, card_cvc)
    if not valid_payment_details:
        flash(payment_error_message, 'error')
        return redirect(url_for('bookings.checkout'))

    # Assume that listing_id and user_id are obtained from session or form
    cache = session['checkout_cache']
    listing_id = cache['listing_id']
    user_id = g.identity.id
    num_seats = int(cache['num_seats'])
    seat_type = cache['seat_type']
    per_person_cost = cache['per_person_cost']
    total_cost = per_person_cost * num_seats

    depart_date = cache['depart_date']
    last_four_card_nums = card_number[-4:]

    # Convert depart_date to date object
    depart_date_obj = datetime.strptime(depart_date, '%Y-%m-%d').date()

    availability = ListingAvailability.check_availability(listing_id, depart_date_obj, seat_type, num_seats)
    if availability != True:
        flash(f"Not enough seats available. There are {availability} remaining seats for {seat_type.capitalize()}.", 'error')
        return redirect(url_for('bookings.listing', id=listing_id))

    try:
        booking = Bookings.create_booking(listing_id, user_id, total_cost, seat_type, num_seats, depart_date, last_four_card_nums)
        if booking:
            # Update availability
            ListingAvailability.update_availability(listing_id, depart_date_obj, seat_type, num_seats)
            db.session.commit()
            flash('Booking successful!', 'success')
        else:
            flash('Booking failed. Please try again.', 'error')
            return redirect(url_for('bookings.checkout'))
    except Exception as e:
        db.session.rollback()
        error_logger.debug(f"Error processing booking: {e}")
        flash('Booking failed. Please try again.', 'error')
        return redirect(url_for('bookings.checkout'))

    return redirect(url_for('bookings.payment_complete', id=booking.id))


def validate_payment(card_number, card_expiry, card_cvc):
    if len(card_number) != 16 or not card_number.isdigit():
        return False, "Invalid card number. It must be 16 digits."
    
    if len(card_cvc) != 3 or not card_cvc.isdigit():
        return False, "Invalid CVC. It must be 3 digits."

    try:
        exp_month, exp_year = card_expiry.split('/')
        exp_month = int(exp_month)
        exp_year = int(exp_year) + 2000 
        expiry_date = datetime(exp_year, exp_month, 1)
        if expiry_date < datetime.now():
            return False, "Card expiry date cannot be in the past."
    except ValueError:
        return False, "Invalid expiry date format. It must be MM/YY."

    return True, 'Success'

@bp.route('/filter_bookings', methods=['POST'])
def filter_bookings():
    # Get filter criteria from the request
    data = request.get_json()
    depart_location = data.get('depart_location', [])
    destination_location = data.get('destination_location', [])
    depart_date = data.get('date')
    seat_type = data.get('seatType', 'economy')
    page = int(data.get('page', 1)) 
    per_page = 10  # How many listings show per page

    discount, days_away = calculate_discount(depart_date)

    query = db.session.query(Listings)

    if depart_location:
        query = query.filter(Listings.depart_location.in_(depart_location))
    if destination_location:
        query = query.filter(Listings.destination_location.in_(destination_location))

    filtered_items = query.all()
    total_items = len(filtered_items)

    # Ignore pagination if any filters are applied
    if depart_location or destination_location:
        paginated_items = filtered_items 
        page = 1 
        total_pages = 1
    else:
        # Paginate the results
        paginated_items = filtered_items[(page - 1) * per_page: page * per_page]
        total_pages = (total_items + per_page - 1) // per_page

    # Calculate total cost and apply discount
    for item in paginated_items:
        if seat_type == 'economy':
            item.discounted_cost = item.economy_fair_cost * (1 - discount / 100)
            item.original_cost = item.economy_fair_cost
        elif seat_type == 'business':
            item.discounted_cost = item.business_fair_cost * (1 - discount / 100)
            item.original_cost = item.business_fair_cost

    # Process images
    process_images(paginated_items)

    # Render only the relevant portion of the results
    results_html = render_template('_results.html', items=paginated_items, page=page, total_pages=total_pages, discount=discount, days_away=days_away, seat_type=seat_type)
    return jsonify({'html': results_html})

def process_images(listings):
    for item in listings:
        main_image = next((img for img in item.listing_images if img.main_image), None)
        if main_image:
            item.main_image_url = url_for('main.upload_file', filename=main_image.image_location)
        elif item.listing_images:
            item.main_image_url = url_for('main.upload_file', filename=item.listing_images[0].image_location)
        else:
            item.main_image_url = url_for('main.upload_file', filename='booking_image_not_found.jpg')
        # Must be a single quote JSON otherwise doesn't work in frontend
        item.image_urls = json.dumps([url_for('main.upload_file', filename=img.image_location) for img in item.listing_images]).replace('"', '&quot;')


@bp.route('/payment_success/<int:id>')
def payment_success(booking_id):
    return render_template('payment_success.html', booking_id=booking_id)

@bp.route('/generate-receipt/<int:id>')
def generate_receipt(id):
    booking = Bookings.search_booking(id)
    listing = Listings.search_listing(booking.listing_id)
    pdf = create_receipt(booking, listing)
    
    return send_file(pdf, as_attachment=True, download_name='receipt.pdf')

@bp.route('/generate-ticket/<int:id>')
def generate_ticket(id):
    booking = Bookings.search_booking(id)
    listing = Listings.search_listing(booking.listing_id)
    
    pdf = create_plane_ticket(booking, listing)
    
    return send_file(pdf, as_attachment=True, download_name='plane_ticket.pdf')

@bp.route('/get_user_bookings', methods=['GET'])
@permission_required(user_permission)
def get_user_bookings():
    query = db.session.query(Bookings).join(Listings)
    
    query = query.filter(Bookings.user_id == current_user.id)

    depart_location = request.args.get('depart_location')
    destination_location = request.args.get('destination_location')
    booking_date = request.args.get('booking_date')
    depart_date = request.args.get('depart_date')
    exclude_cancelled = request.args.get('exclude_cancelled')

    if exclude_cancelled and exclude_cancelled.lower() == 'true':
        query = query.filter(Bookings.cancelled == 0)

    if depart_location:
        depart_locations = depart_location.split(',')
        query = query.filter(Listings.depart_location.in_(depart_locations))
    if destination_location:
        destination_locations = destination_location.split(',')
        query = query.filter(Listings.destination_location.in_(destination_locations))
    if booking_date:
        query = query.filter(Bookings.booking_date == booking_date)
    if depart_date:
        query = query.filter(Bookings.depart_date == depart_date)

    filtered_data = query.all()
    result = [
        {
            'id': booking.id,
            'depart_location': booking.listing.depart_location,
            'booking_date': booking.booking_date.strftime("%a, %d %b %Y"),
            'destination_location': booking.listing.destination_location,
            'depart_date': booking.depart_date.strftime("%a, %d %b %Y"),
            'cancelled': 'Yes' if booking.cancelled else 'No'
        } for booking in filtered_data
    ]
    
    return jsonify(result)


@bp.route('/cancel_booking/<int:id>', methods=['POST'])
@permission_required(user_permission)
def cancel_booking(id):
    if not id:
        flash('Unable to cancel booking', 'error')
        return redirect(url_for('bookings.manage_bookings'))
    
    booking = Bookings.search_booking(id)
    cancel_amount, cancel_percentage = calculate_refund_amount(booking)
    success = Bookings.cancel_booking(id, cancel_amount)
    if success:
        flash('Your booking has been successfully cancelled. If you are entitled to a refund this will be refunded to your payment card', 'success')
        return redirect(url_for('profile.manage_bookings'))
    else:
        flash('Unable to cancel booking, please try again', 'error')
        return redirect(url_for('profile.manage_profile_view_booking', id=id))