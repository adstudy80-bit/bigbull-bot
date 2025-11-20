from flask import Flask, request, jsonify
from flask_cors import CORS
import asyncio
import time
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

class EmoteBot:
    def __init__(self):
        self.command_history = []
        self.bot_status = "ready"
        logger.info("🎭 EMOTE BOT Initialized")
    
    async def process_command(self, command):
        """Process commands from Netflixy website"""
        logger.info(f"📱 Received command: {command}")
        
        # Add to history
        self.command_history.append({
            'command': command,
            'timestamp': time.time(),
            'status': 'processing'
        })
        
        # Process different command types
        if command.startswith('!e'):
            return await self.handle_emote(command)
        elif command.startswith('/x/'):
            return await self.handle_team_join(command)
        elif command == '/5':
            return await self.handle_squad_create()
        elif command == '/solo':
            return await self.handle_squad_leave()
        elif command == '/s':
            return await self.handle_matchmaking()
        elif command in ('/help', 'help'):
            return self.get_help_text()
        else:
            return f"❓ Unknown command: {command}"
    
    async def handle_emote(self, command):
        """Process emote command: !e [UID] [EMOTE_ID]"""
        try:
            parts = command.split()
            if len(parts) >= 3:
                uid = parts[1]
                emote_id = parts[2]
                
                # Validate UID and emote ID
                if not uid.isdigit():
                    return "❌ Invalid UID format"
                if not emote_id.isdigit():
                    return "❌ Invalid Emote ID format"
                
                # Here you would integrate with your actual Nm.py bot
                # For now, simulate successful execution
                logger.info(f"🎭 Executing emote {emote_id} on UID: {uid}")
                
                return f"✅ Emote {emote_id} executed on player: {uid}"
            else:
                return "❌ Invalid format. Use: !e [UID] [EMOTE_ID]"
                
        except Exception as e:
            logger.error(f"Error in handle_emote: {e}")
            return f"❌ Error processing emote command: {str(e)}"
    
    async def handle_team_join(self, command):
        """Process team join command: /x/ [TEAM_CODE]"""
        try:
            team_code = command.split('/x/')[1].strip()
            if not team_code:
                return "❌ Please provide team code"
            
            logger.info(f"🎯 Joining team: {team_code}")
            
            # Simulate team join
            return f"✅ Joining team with code: {team_code}"
            
        except Exception as e:
            logger.error(f"Error in handle_team_join: {e}")
            return f"❌ Error joining team: {str(e)}"
    
    async def handle_squad_create(self):
        """Create 5-player squad"""
        logger.info("👥 Creating 5-player squad")
        return "✅ 5-player squad created successfully"
    
    async def handle_squad_leave(self):
        """Leave current squad"""
        logger.info("🚪 Leaving squad")
        return "✅ Left current squad"
    
    async def handle_matchmaking(self):
        """Start matchmaking"""
        logger.info("🎮 Starting matchmaking")
        return "✅ Matchmaking started"
    
    def get_help_text(self):
        """Return help text"""
        return """
🤖 EMOTE BOT - Available Commands:

🎭 EMOTES:
  !e [UID] [EMOTE_ID] - Perform emote on player
  Example: !e 123456789 909000001

🎯 TEAM:
  /x/ [TEAM_CODE] - Bot join your team
  Example: /x/ ABC123

👥 SQUAD:
  /5 - Create 5-player squad
  /solo - Leave current squad
  /s - Start matchmaking

📞 HELP:
  /help - Show this message

🌐 Platform: Netflixy + Katabump
👨‍💻 Developer: ABHI THE BIG BULL
"""

# Initialize bot
emote_bot = EmoteBot()

@app.route('/')
def home():
    """Root endpoint"""
    return jsonify({
        "status": "online",
        "message": "🎭 EMOTE BOT API - BIG BULL",
        "version": "1.0",
        "endpoints": {
            "/execute": "POST - Execute bot commands",
            "/status": "GET - Check bot status",
            "/history": "GET - Command history"
        },
        "developer": "ABHI THE BIG BULL"
    })

@app.route('/execute', methods=['POST'])
def execute_command():
    """Execute commands from Netflixy website"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "status": "error", 
                "message": "❌ No JSON data received"
            })
        
        command = data.get('command', '').strip()
        user = data.get('user', 'netflixy_user')
        
        if not command:
            return jsonify({
                "status": "error",
                "message": "❌ No command provided"
            })
        
        # Process command asynchronously
        result = asyncio.run(emote_bot.process_command(command))
        
        logger.info(f"✅ Command processed: {command}")
        
        return jsonify({
            "status": "success",
            "message": "✅ Command executed successfully",
            "result": result,
            "command": command,
            "user": user,
            "timestamp": time.time()
        })
        
    except Exception as e:
        logger.error(f"❌ Server error: {e}")
        return jsonify({
            "status": "error",
            "message": f"❌ Server error: {str(e)}"
        })

@app.route('/status', methods=['GET'])
def get_status():
    """Check bot status"""
    return jsonify({
        "status": "online",
        "bot": "🎭 EMOTE BOT",
        "platform": "Katabump",
        "website": "Netflixy",
        "commands_processed": len(emote_bot.command_history),
        "last_command": emote_bot.command_history[-1] if emote_bot.command_history else None,
        "timestamp": time.time()
    })

@app.route('/history', methods=['GET'])
def get_history():
    """Get command history"""
    return jsonify({
        "status": "success",
        "history": emote_bot.command_history[-10:],  # Last 10 commands
        "total_commands": len(emote_bot.command_history)
    })

@app.route('/test', methods=['GET'])
def test_connection():
    """Test connection endpoint"""
    return jsonify({
        "status": "success",
        "message": "🎭 EMOTE BOT is working!",
        "connection": "Netflixy ↔ Katabump ✅",
        "timestamp": time.time()
    })

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "emote_bot_api"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    
    print("🚀 Starting EMOTE BOT API...")
    print("🎭 Bot: EMOTE BOT - BIG BULL")
    print("🌐 Website: Netflixy")
    print("🖥️  Hosting: Katabump")
    print("👨‍💻 Developer: ABHI THE BIG BULL")
    print(f"📍 Port: {port}")
    print("\n📋 Available Endpoints:")
    print("   POST /execute - Execute commands")
    print("   GET  /status  - Check bot status")
    print("   GET  /history - Command history")
    print("   GET  /test    - Test connection")
    print("   GET  /health  - Health check")
    
    app.run(host='0.0.0.0', port=port, debug=False)