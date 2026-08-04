from flask import Flask, request, jsonify
from flask_cors import CORS
from graph.Chatbot_graph import validation_graph
from db.DBConnection import getConnection
from rag.vectorstore import get_retriever
from nodes.retrieve_schema import retrieve_schema
from dotenv import load_dotenv
import logging
from functools import wraps
import os
from datetime import datetime
import traceback

# ============================================================================
# CONFIGURATION
# ============================================================================

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============================================================================
# APP INITIALIZATION
# ============================================================================

app = Flask(__name__)

# Configuration
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# CORS Configuration
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# ============================================================================
# GLOBAL INITIALIZATION
# ============================================================================

try:
    logger.info("Initializing vector retriever...")
    retriever = get_retriever()
    logger.info("Vector retriever initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize vector retriever: {str(e)}")
    retriever = None

# ============================================================================
# DECORATORS
# ============================================================================

def handle_errors(f):
    """Decorator for consistent error handling."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {f.__name__}: {str(e)}")
            logger.error(traceback.format_exc())
            return jsonify({
                "success": False,
                "error": "Internal server error",
                "message": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }), 500
    return decorated_function

def validate_json(required_fields=None):
    """Decorator to validate JSON request data."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                return jsonify({
                    "success": False,
                    "error": "Invalid request",
                    "message": "Content-Type must be application/json"
                }), 400
            
            data = request.get_json()
            
            if required_fields:
                missing_fields = [field for field in required_fields if field not in data]
                if missing_fields:
                    return jsonify({
                        "success": False,
                        "error": "Missing required fields",
                        "missing_fields": missing_fields
                    }), 400
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def create_response(success=True, data=None, error=None, message=None, status_code=200):
    """Create a standardized API response."""
    response = {
        "success": success,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    if data is not None:
        response["data"] = data
    if error:
        response["error"] = error
    if message:
        response["message"] = message
    
    return jsonify(response), status_code

def execute_query(query, params=None, fetch_one=False):
    """Execute a database query with proper error handling."""
    conn = None
    cursor = None
    
    try:
        conn = getConnection()
        cursor = conn.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if fetch_one:
            result = cursor.fetchone()
        else:
            result = cursor.fetchall()
        
        conn.commit()
        return result
    
    except Exception as e:
        logger.error(f"Database error: {str(e)}")
        if conn:
            conn.rollback()
        raise
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# ============================================================================
# ROUTES
# ============================================================================

@app.route("/")
@handle_errors
def index():
    """Root endpoint."""
    return create_response(
        success=True,
        data={
            "service": "SQL AI Agent API",
            "version": "1.0.0",
            "status": "running"
        }
    )

@app.route("/health", methods=["GET"])
@handle_errors
def health():
    """Health check endpoint."""
    health_status = {
        "status": "healthy",
        "services": {
            "api": "operational",
            "database": "unknown",
            "retriever": "operational" if retriever else "unavailable"
        }
    }
    
    # Check database connection
    try:
        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        conn.close()
        health_status["services"]["database"] = "operational"
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        health_status["services"]["database"] = "unavailable"
        health_status["status"] = "degraded"
    
    status_code = 200 if health_status["status"] == "healthy" else 503
    return create_response(
        success=health_status["status"] == "healthy",
        data=health_status,
        status_code=status_code
    )

@app.route("/getAnswer", methods=["POST"])
@handle_errors
@validate_json(required_fields=["question"])
def answer():
    """
    Process natural language question and return SQL query results.
    
    Expected JSON:
    {
        "question": "Your question here",
        "user_type": "user" (optional)
    }
    """
    logger.info("Received query request")
    
    data = request.get_json()
    question = data.get("question", "").strip()
    user_type = data.get("user_type", "user")
    
    # Validate question
    if not question:
        return create_response(
            success=False,
            error="Invalid question",
            message="Question cannot be empty",
            status_code=400
        )
    
    if len(question) > 1000:
        return create_response(
            success=False,
            error="Question too long",
            message="Question must be less than 1000 characters",
            status_code=400
        )
    
    logger.info(f"Processing question: {question[:100]}...")
    
    try:
        # Initialize and invoke workflow
        workflow = validation_graph()
        result = workflow.invoke({
            "input": question,
            "user_type": user_type
        })
        
        logger.info("Workflow completed successfully")
        
        # Prepare response data
        response_data = {
            "success": True,
            "question": question,
            "query": result.get("query", ""),
            "query_result": result.get("query_result"),
            "summary": result.get("summary"),
            "result": result.get("result"),
            "error": result.get("Error") or result.get("database_error"),
            "has_query": bool(result.get("query", "").strip()),
            "has_error": bool(result.get("Error") or result.get("database_error"))
        }
        
        # Remove None values for cleaner response
        response_data = {k: v for k, v in response_data.items() if v is not None and v != ""}
        
        return jsonify(response_data), 200
    
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}")
        logger.error(traceback.format_exc())
        
        return jsonify({
            "success": False,
            "error": "Processing failed",
            "message": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }), 500

@app.route("/getAllDetails", methods=["GET"])
@handle_errors
def getCustomerDetails():
    """Retrieve all customer details."""
    logger.info("Fetching all customers")
    
    try:
        data = execute_query("SELECT * FROM customers")
        
        return create_response(
            success=True,
            data={
                "customers": data if data else [],
                "count": len(data) if data else 0
            }
        )
    
    except Exception as e:
        logger.error(f"Error fetching customers: {str(e)}")
        return create_response(
            success=False,
            error="Database error",
            message=str(e),
            status_code=500
        )

@app.route("/getSchema", methods=["GET"])
@handle_errors
def get_schema():
    """Retrieve database schema information."""
    logger.info("Fetching database schema")
    
    try:
        schema = retrieve_schema()
        return create_response(
            success=True,
            data={"schema": schema}
        )
    
    except Exception as e:
        logger.error(f"Error fetching schema: {str(e)}")
        return create_response(
            success=False,
            error="Schema retrieval failed",
            message=str(e),
            status_code=500
        )

@app.route("/getStats", methods=["GET"])
@handle_errors
def get_stats():
    """Get database statistics."""
    try:
        stats = {}
        
        # Get table counts - adjust table names based on your schema
        tables = ["customers", "orders", "products"]
        for table in tables:
            try:
                result = execute_query(f"SELECT COUNT(*) FROM {table}", fetch_one=True)
                stats[table] = result[0] if result else 0
            except:
                stats[table] = 0
        
        return create_response(
            success=True,
            data={"statistics": stats}
        )
    
    except Exception as e:
        logger.error(f"Error fetching stats: {str(e)}")
        return create_response(
            success=False,
            error="Failed to fetch statistics",
            message=str(e),
            status_code=500
        )

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return create_response(
        success=False,
        error="Not found",
        message="The requested endpoint does not exist",
        status_code=404
    )

@app.errorhandler(405)
def method_not_allowed(error):
    return create_response(
        success=False,
        error="Method not allowed",
        message="The method is not allowed for the requested URL",
        status_code=405
    )

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {str(error)}")
    return create_response(
        success=False,
        error="Internal server error",
        message="An unexpected error occurred",
        status_code=500
    )

# ============================================================================
# REQUEST HANDLERS
# ============================================================================

@app.before_request
def log_request():
    """Log incoming requests."""
    logger.info(f"{request.method} {request.path} - {request.remote_addr}")

@app.after_request
def after_request(response):
    """Add security headers."""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_ENV", "development") == "development"
    
    logger.info(f"Starting Flask app on port {port}")
    logger.info(f"Debug mode: {debug}")
    
    app.run(
        host="0.0.0.0",
        port=port,
        debug=debug,
        threaded=True
    )