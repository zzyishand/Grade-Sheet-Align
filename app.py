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
        
        # 获取输入数据  
        standard_col = data['standard_col']  
        align_col = data['align_col']  
        score_col = data['score_col']  

        # 清理和分割数据  
        standard_lines = [line.strip() for line in standard_col.split('\n') if line.strip()]  
        align_lines = [line.strip() for line in align_col.split('\n') if line.strip()]  
        score_lines = [line.strip() for line in score_col.split('\n') if line.strip()]  

        # 清除可能存在的序号  
        standard_lines = [re.sub(r'^No\.\d+\s+', '', line) for line in standard_lines]  
        align_lines = [re.sub(r'^No\.\d+\s+', '', line) for line in align_lines]  

        # 创建带序号的标准列表  
        numbered_standard = [f"No.{i+1} {line}" for i, line in enumerate(standard_lines)]  

        # 创建对齐映射  
        align_map = dict(zip(align_lines, score_lines))  

        # 根据标准列表重新排序分数  
        result = []  
        not_found = []  
        for std_line in standard_lines:  
            if std_line in align_map:  
                result.append(align_map[std_line])  
            else:  
                not_found.append(std_line)  

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