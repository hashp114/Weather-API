from flask import request, jsonify
from flask_restful import Resource
from models import WeatherData

class WeatherResource(Resource):
    def get(self):
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        station_id = request.args.get('station_id', type=int)
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        filters = []
        if station_id:
            filters.append(WeatherData.station_id == station_id)
        if start_date and end_date:
            filters.append(WeatherData.date.between(start_date, end_date))

        query = WeatherData.query.filter(*filters)

        # Total count of items to compute total pages and limit for results
        total_items = query.count()

        # Calculate the limit and offset for the query
        offset = (page - 1) * per_page
        query = query.offset(offset).limit(per_page)

        items = query.all()

        data = []
        for item in items:
            data.append({
                'date': item.date.isoformat(),
                'max_temp': item.max_temp,
                'min_temp': item.min_temp,
                'precipitation': item.precipitation,
                'station_id': item.station_id,
                'file_name': item.file_name,
                'file_load_date': item.file_load_date.isoformat()
            })

        return jsonify({
            'total': total_items,
            'pages': (total_items + per_page - 1) // per_page,  # Calculate total pages
            'page': page,
            'per_page': per_page,
            'data': data
        })
