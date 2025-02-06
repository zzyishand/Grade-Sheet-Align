from flask import Flask, render_template, request, jsonify  

app = Flask(__name__)  

@app.route('/')  
def index():  
    return render_template('index.html')  

@app.route('/align', methods=['POST'])  
def align():  
    try:  
        standard_col = request.json['standard_col'].strip().split('\n')  
        align_col = request.json['align_col'].strip().split('\n')  
        score_col = request.json['score_col'].strip().split('\n')  

        # Add numbering to standard column  
        numbered_standard = [f"No.{i+1} {line.strip()}" for i, line in enumerate(standard_col)]  
        
        # Create alignment mapping  
        align_score_dict = dict(zip(align_col, score_col))  
        
        # Realign scores based on standard column  
        result = []  
        not_found = []  
        
        for item in standard_col:  
            item = item.strip()  
            if item in align_col:  
                result.append(align_score_dict[item])  
            else:  
                result.append('')  
                not_found.append(item)  

        return jsonify({  
            'success': True,  
            'result': result,  
            'not_found': not_found,  
            'numbered_standard': numbered_standard,  
            'total_rows': len(standard_col)  
        })  

    except Exception as e:  
        return jsonify({  
            'success': False,  
            'error': str(e)  
        })  

if __name__ == '__main__':  
    app.run(debug=True)