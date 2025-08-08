from app import create_app
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create Flask app
app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    print(f"🚀 Starting Credit Score Analysis API on port {port}")
    print(f"📊 Debug mode: {debug}")
    print(f"🔐 Auth bypass: {app.config.get('BYPASS_AUTH', False)}")
    print(f"🗄️ MongoDB URI: {app.config.get('MONGO_URI')}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
