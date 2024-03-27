from flask import Blueprint, jsonify

bp = Blueprint('admin', __name__)

@bp.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'It is working!'}), 200
