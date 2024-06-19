from flask import request, jsonify
from flask_restful import Resource
import logging
from models import StationYearlyStatistics

class WeatherStatsResource(Resource):
    def get(self):
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        station_name = request.args.get('station_name')
        year = request.args.get('year', type=int)
        
        filters = []
        if station_name:
            filters.append(StationYearlyStatistics.station_name == station_name)
        if year:
            filters.append(StationYearlyStatistics.year == year)
        
        query = StationYearlyStatistics.query.filter(*filters)
        
        logging.info(f"Executing query: {query}")
        
        # Total count of items to compute total pages and limit for results
        total_items = query.count()
        logging.info(f"Total items found: {total_items}")
        
        # Calculate the limit and offset for the query
        offset = (page - 1) * per_page
        query = query.offset(offset).limit(per_page)
        
        items = query.all()
        
        data = []
        for item in items:
            data.append({
                'station_name': item.station_name,
                'year': item.year,
                'avg_max_temp': item.avg_max_temp,
                'avg_min_temp': item.avg_min_temp,
                'total_precipitation': item.total_precipitation,
                'row_key': item.row_key
            })
        
        return jsonify({
            'total': total_items,
            'pages': (total_items + per_page - 1) // per_page,  # Calculate total pages
            'page': page,
            'per_page': per_page,
            'data': data
        })