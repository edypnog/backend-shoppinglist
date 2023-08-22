from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# Configuração do banco de dados (substitua pelos detalhes do seu banco)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class TodoItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)


@app.route('/api/get_all_items', methods=['GET'])
def get_all_items():
    items = TodoItem.query.all()
    item_list = []
    for item in items:
        item_list.append({
            'id': item.id,
            'text': item.text,
            'completed': item.completed
        })
    return jsonify({'items': item_list})


@app.route('/api/add_item', methods=['POST'])
def add_item():
    data = request.json

    new_item = TodoItem(text=data['text'], completed=False)
    db.session.add(new_item)
    db.session.commit()

    return jsonify({'message': 'Item added successfully'})


@app.route('/api/update_item/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = TodoItem.query.get(item_id)
    if not item:
        return jsonify({'error': 'Item not found'}), 404

    item.text = request.json.get('text', item.text)
    item.completed = request.json.get('completed', item.completed)

    db.session.commit()
    return jsonify({'message': 'Item updated successfully'})


@app.route('/api/delete_item/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = TodoItem.query.get(item_id)
    if not item:
        return jsonify({'error': 'Item not found'}), 404

    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Item deleted successfully'})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
