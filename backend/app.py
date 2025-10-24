from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from prometheus_flask_exporter import PrometheusMetrics
import os
import logging
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://user:password@postgres:5432/taskdb')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

# Initialize extensions
db = SQLAlchemy(app)
metrics = PrometheusMetrics(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database Models
class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(50), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

# Routes
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for Kubernetes probes"""
    try:
        # Check database connection
        db.session.execute('SELECT 1')
        return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()}), 200
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 503

@app.route('/ready', methods=['GET'])
def readiness_check():
    """Readiness check endpoint for Kubernetes"""
    return jsonify({'status': 'ready'}), 200

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks"""
    try:
        tasks = Task.query.all()
        return jsonify([task.to_dict() for task in tasks]), 200
    except Exception as e:
        logger.error(f"Error fetching tasks: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Get a specific task"""
    task = Task.query.get_or_404(task_id)
    return jsonify(task.to_dict()), 200

@app.route('/api/tasks', methods=['POST'])
def create_task():
    """Create a new task"""
    try:
        data = request.get_json()
        
        if not data or 'title' not in data:
            return jsonify({'error': 'Title is required'}), 400
        
        task = Task(
            title=data['title'],
            description=data.get('description', ''),
            status=data.get('status', 'pending')
        )
        
        db.session.add(task)
        db.session.commit()
        
        logger.info(f"Created task: {task.id}")
        return jsonify(task.to_dict()), 201
    except Exception as e:
        logger.error(f"Error creating task: {str(e)}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update a task"""
    try:
        task = Task.query.get_or_404(task_id)
        data = request.get_json()
        
        if 'title' in data:
            task.title = data['title']
        if 'description' in data:
            task.description = data['description']
        if 'status' in data:
            task.status = data['status']
        
        db.session.commit()
        logger.info(f"Updated task: {task.id}")
        return jsonify(task.to_dict()), 200
    except Exception as e:
        logger.error(f"Error updating task: {str(e)}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task"""
    try:
        task = Task.query.get_or_404(task_id)
        db.session.delete(task)
        db.session.commit()
        logger.info(f"Deleted task: {task_id}")
        return jsonify({'message': 'Task deleted successfully'}), 200
    except Exception as e:
        logger.error(f"Error deleting task: {str(e)}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def index():
    """Root endpoint"""
    return jsonify({
        'message': 'DevOps Task Manager API',
        'version': '1.0.0',
        'endpoints': {
            'health': '/health',
            'ready': '/ready',
            'tasks': '/api/tasks',
            'metrics': '/metrics'
        }
    }), 200

# Database initialization
@app.before_first_request
def create_tables():
    """Create database tables"""
    db.create_all()
    logger.info("Database tables created")

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
