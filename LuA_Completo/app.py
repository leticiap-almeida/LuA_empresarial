from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask import jsonify

app = Flask(__name__)
app.secret_key = 'segredo123'

usuarios = {
    'admin': '1234',
}

produtos = []

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        module = request.form['module']

        if username in usuarios and usuarios[username] == password:
            session['user'] = username
            if module == 'financeiro':
                return redirect(url_for('financeiro'))
            elif module == 'estoque':
                return redirect(url_for('estoque'))
            elif module == 'orcamentos':
                return redirect(url_for('orcamentos'))
            else:
                flash("Módulo inválido.")
        else:
            flash("Usuário ou senha incorretos.")
    return render_template('login.html')

@app.route('/financeiro')
def financeiro():
    return render_template('financeiro.html')

@app.route('/estoque')
def estoque():
    return render_template('estoque.html', produtos=produtos)

@app.route('/estoque/adicionar', methods=['GET', 'POST'])
def adicionar_produto():
    if request.method == 'POST':
        novo_produto = {
            'id': len(produtos) + 1,
            'nome': request.form['descricao'],
            'quantidade': request.form['quantidade'],
            'valor_custo': request.form['valor_custo'],
            'valor_venda': request.form['valor_venda'],
            'unidade': request.form['unidade']
        }
        produtos.append(novo_produto)
        return redirect(url_for('estoque'))
    return render_template('adicionar_produto.html')

@app.route('/estoque/editar/<int:produto_id>', methods=['GET', 'POST'])
def editar_produto(produto_id):
    produto = next((p for p in produtos if p['id'] == produto_id), None)
    if not produto:
        return "Produto não encontrado", 404

    if request.method == 'POST':
        produto['nome'] = request.form['descricao']
        produto['quantidade'] = request.form['quantidade']
        produto['valor_custo'] = request.form['valor_custo']
        produto['valor_venda'] = request.form['valor_venda']
        produto['unidade'] = request.form['unidade']
        return redirect(url_for('estoque'))

    return render_template('editar_produto.html', produto=produto)

@app.route('/estoque/excluir/<int:produto_id>')
def excluir_produto(produto_id):
    global produtos
    produtos = [p for p in produtos if p['id'] != produto_id]
    return redirect(url_for('estoque'))

@app.route('/orcamentos')
def orcamentos():
    return render_template('orcamento.html', produtos=produtos)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
