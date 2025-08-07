from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
from simple_spreadsheet import read_spreadsheet, parse_cell, cell_to_index, read_cell

# Create Flask app with static file serving
app = Flask(__name__, static_folder='static', static_url_path='/static')
CORS(app)  # Enable CORS for all routes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/evaluate', methods=['POST'])
def evaluate_spreadsheet():
    """
    Evaluate a spreadsheet matrix and return the results
    """
    try:
        data = request.json
        matrix = data.get('matrix', [])
        
        if not matrix:
            return jsonify({
                'success': False,
                'error': 'Empty matrix provided'
            }), 400
        
        # Evaluate the spreadsheet
        result = read_spreadsheet(matrix)
        
        return jsonify({
            'success': True,
            'result': result,
            'original': matrix
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/parse_cell', methods=['POST'])
def parse_cell_api():
    """
    Parse a single cell and return its components
    """
    try:
        data = request.json
        cell_content = data.get('cell', '')
        
        ref1, op, ref2 = parse_cell(cell_content)
        
        return jsonify({
            'success': True,
            'ref1': ref1,
            'operator': op,
            'ref2': ref2
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/cell_to_index', methods=['POST'])
def cell_to_index_api():
    """
    Convert cell reference to matrix indices
    """
    try:
        data = request.json
        cell_ref = data.get('cell_ref', '')
        
        indices = cell_to_index(cell_ref)
        
        return jsonify({
            'success': True,
            'row': indices[0],
            'col': indices[1]
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/read_cell', methods=['POST'])
def read_cell_api():
    """
    Evaluate a single cell in context of a spreadsheet
    """
    try:
        data = request.json
        cell_content = data.get('cell', '')
        matrix = data.get('matrix', [])
        
        if not matrix:
            return jsonify({
                'success': False,
                'error': 'Matrix is required'
            }), 400
        
        result = read_cell(cell_content, matrix)
        
        return jsonify({
            'success': True,
            'result': result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
