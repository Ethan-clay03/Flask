from flask import render_template, redirect, url_for, request, jsonify, session, flash
from app.bookings import bp
from app.models import Listings
from app import db
from app.logger import error_logger
from app.main.utils import calculate_discount, pretty_time
import json
from datetime import datetime


@bp.route('/')
def redirect_index():
    return redirect(url_for('bookings.index'), code=301)


@bp.route('/listings')
def listings():
    depart_location = request.args.get('departLocation')
    destination_location = request.args.get('destinationLocation')
    depart_date = request.args.get('departDate')

    page = request.args.get('page', 1, type=int)
    per_page = 10

    # Calculate discount based on departure date
    discount, days_away = calculate_discount(depart_date) if depart_date else (0, 0)

    all_listings = Listings.get_all_listings()

    if depart_location:
        all_listings = [listing for listing in all_listings if listing.depart_location == depart_location]
    if destination_location:
        all_listings = [listing for listing in all_listings if listing.destination_location == destination_location]

    # Calculate pagination items and how many listings exist
    total_items = len(all_listings)
    paginated_listings = all_listings[(page - 1) * per_page: page * per_page]

    process_images(paginated_listings)

    # Get all locations for dropdowns
    locations = Listings.get_all_locations(True)

    return render_template('bookings/listings.html',
                           items=paginated_listings,
                           page=page,
                           total_pages=(total_items + per_page - 1) // per_page,
                           locations=locations,
                           discount=discount,
                           days_away=days_away,
                           form_data={
                               'departLocation': depart_location,
                               'destinationLocation': destination_location
                           }
    )

@bp.route('/listing/apply_update', methods=['POST'])
def listing_apply_update(): 
    data = request.get_json()
    selected_date = data.get('date')
    discount, days_away = calculate_discount(selected_date)

    response = {
        'discount': discount,
        'days_away': days_away
    }
    return jsonify(response)

@bp.route('/checkout')
def checkout(): 
    if not session['checkout_cache']:
        flash("Please select a booking", 'error')
    depart_date = session['checkout_cache']['depart_date']
    num_seats = session['checkout_cache']['num_seats']
    listing_id = session['checkout_cache']['listing_id']

    session['checkout_cache'] = {
        'depart_date': depart_date,
        'num_seats': num_seats,
        'listing_id': listing_id
    }

    listing = Listings.search_listing(listing_id)
    listing.depart_time = pretty_time(listing.depart_time)
    listing.destination_time = pretty_time(listing.destination_time)
    
    # Parse depart_date as a date object
    depart_date_obj = datetime.strptime(depart_date, '%Y-%m-%d')
    depart_date_formatted = depart_date_obj.strftime('%d-%m-%Y')

    return render_template('bookings/checkout.html', listing=listing, num_seats=num_seats, depart_date=depart_date_formatted)

@bp.route('/payment')
def payment(): 
    depart_date = request.args.get('date')
    num_seats = request.args.get('seats')
    listing_id = request.args.get('listing_id')

    if not depart_date or not num_seats or not listing_id:
        flash('Please select a booking in order to checkout.', 'error')
        return redirect(url_for('bookings.listings'))

    session['checkout_cache'] = {
        'depart_date': depart_date,
        'num_seats': num_seats,
        'listing_id': listing_id
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
    listing.depart_time = pretty_time(listing.depart_time)
    listing.destination_time = pretty_time(listing.destination_time)
    filter_data = session.pop('filter_data', None)

    selected_date = filter_data['date'] if filter_data and 'date' in filter_data else None
    discount, days_away = calculate_discount(selected_date) if selected_date else (0, 0)

    return render_template('bookings/listing.html', listing=listing, selected_date=selected_date, discount=discount, days_away=days_away)


@bp.route('/filter_bookings', methods=['POST'])
def filter_bookings():
    try:
        # Get filter criteria from the request
        data = request.get_json()
        depart_location = data.get('depart_location', [])
        destination_location = data.get('destination_location', [])
        min_fair_cost = data.get('min_fair_cost')
        max_fair_cost = data.get('max_fair_cost')
        depart_date = data.get('date')
        page = int(data.get('page', 1))  # Get the page parameter or default to 1
        per_page = 10  # How many listings show per page

        discount, days_away = calculate_discount(depart_date)

        query = db.session.query(Listings)

        if depart_location:
            query = query.filter(Listings.depart_location.in_(depart_location))
        if destination_location:
            query = query.filter(Listings.destination_location.in_(destination_location))
        if min_fair_cost:
            query = query.filter(Listings.fair_cost >= float(min_fair_cost))
        if max_fair_cost:
            query = query.filter(Listings.fair_cost <= float(max_fair_cost))

        filtered_items = query.all()
        total_items = len(filtered_items)

        # Ignore pagination if any filters are applied
        if depart_location or destination_location or min_fair_cost or max_fair_cost:
            paginated_items = filtered_items 
            page = 1 
            total_pages = 1
        else:
            # Paginate the results
            paginated_items = filtered_items[(page - 1) * per_page: page * per_page]
            total_pages = (total_items + per_page - 1) // per_page

        # Process images
        process_images(paginated_items)

        # Render only the relevant portion of the results
        results_html = render_template('_results.html', items=paginated_items, page=page, total_pages=total_pages, discount=discount, days_away=days_away)
        return jsonify({'html': results_html})

    except Exception as e:
        error_logger.debug(e)
        return jsonify({'error': str(e)}), 400


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
