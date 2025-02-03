from flask import render_template, redirect, url_for, request, jsonify
from app.bookings import bp
from app.models import Listings
from app import db
from app.logger import error_logger
import json


@bp.route('/')
def redirect_index():
    return redirect(url_for('bookings.index'), code=301)


@bp.route('/listings')
def listings():
    page = request.args.get('page', 1, type=int)
    locations = Listings.get_all_locations(True)
    per_page = 10  # Define how many items per page

    # Assuming get_all_listings returns a list, manually paginate
    all_listings = Listings.get_all_listings()
    total_items = len(all_listings)

    paginated_listings = all_listings[(page - 1) * per_page: page * per_page]

    # Process images
    process_images(paginated_listings)

    return render_template('bookings/listings.html', 
                           items=paginated_listings, 
                           page=page, 
                           total_pages=(total_items + per_page - 1) // per_page,
                           locations=locations)




@bp.route('/listing/<int:id>')
def show_listing(id):
    return render_template('bookings/listings.html', id=1)

@bp.route('/filter', methods=['POST'])
def filter_bookings():
    try:
        # Get filter criteria from the request
        data = request.get_json()
        depart_location = data.get('depart_location', [])
        destination_location = data.get('destination_location', [])
        min_fair_cost = data.get('min_fair_cost')
        max_fair_cost = data.get('max_fair_cost')
        page = int(data.get('page', 1))  # Get the page parameter or default to 1
        per_page = 10  # Define how many items per page

        # Construct the query
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
            paginated_items = filtered_items  # Ignore pagination
            page = 1  # Reset page to 1
            total_pages = 1  # Only one page of results
        else:
            # Paginate the results
            paginated_items = filtered_items[(page - 1) * per_page: page * per_page]
            total_pages = (total_items + per_page - 1) // per_page

        # Process images
        process_images(paginated_items)

        # Render only the relevant portion of the results
        results_html = render_template('_results.html', items=paginated_items, page=page, total_pages=total_pages)
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

