from flask import Flask, render_template, request, jsonify  
import re  

app = Flask(__name__)  

@app.route('/')  
def index():  
    return render_template('index.html')  

@app.route('/align', methods=['POST'])  
def align():  
    try:  
        data = request.get_json()  
        
        # Get input data  
        standard_col = data['standard_col']  
        align_col = data['align_col']  
        score_col = data['score_col']  

        # Clean and split data - remove empty lines more strictly  
        standard_lines = [line.strip() for line in standard_col.split('\n') if line.strip()]  
        align_lines = [line.strip() for line in align_col.split('\n') if line.strip()]  
        score_lines = [line.strip() for line in score_col.split('\n') if line.strip()]  

        # Remove possible numbering  
        standard_lines = [re.sub(r'^No\.\d+\s+', '', line) for line in standard_lines]  
        align_lines = [re.sub(r'^No\.\d+\s+', '', line) for line in align_lines]  

        # Create numbered standard list  
        numbered_standard = [f"No.{i+1} {line}" for i, line in enumerate(standard_lines)]  

        # Create alignment mapping  
        align_map = dict(zip(align_lines, score_lines))  

        # Initialize result array with empty strings (not newlines)  
        result = [''] * len(standard_lines)  
        not_found = []  

        # Fill in scores at matching positions  
        for i, std_line in enumerate(standard_lines):  
            if std_line in align_map:  
                result[i] = align_map[std_line]  
            else:  
                not_found.append(std_line)  
                # Keep as empty string, not newline  

        return jsonify({  
            'success': True,  
            'numbered_standard': numbered_standard,  
            'result': result,  
            'not_found': not_found,  
            'total_rows': len(standard_lines)  
        })  

    except Exception as e:  
        return jsonify({  
            'success': False,  
            'error': str(e)  
        })  

if __name__ == '__main__':  
    app.run(debug=True)  