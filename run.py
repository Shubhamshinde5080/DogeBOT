import uvicorn
from bot.utils.env_mapper import setup_environment
from bot.app import app

# Set up environment variables for Railway.app compatibility
setup_environment()

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)