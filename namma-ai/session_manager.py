import uuid
import json
import os
from datetime import datetime, timedelta
from typing import Dict, Optional

class SessionManager:
    def __init__(self, sessions_file="data/sessions.json"):
        self.sessions_file = sessions_file
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(sessions_file), exist_ok=True)
        self.sessions = self.load_sessions()
    
    def load_sessions(self) -> Dict:
        """Load existing sessions from file"""
        if os.path.exists(self.sessions_file):
            try:
                with open(self.sessions_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_sessions(self):
        """Save sessions to file"""
        with open(self.sessions_file, 'w') as f:
            json.dump(self.sessions, f, indent=2)
    
    def create_session(self) -> str:
        """Create a new session and return session token"""
        session_id = str(uuid.uuid4())[:8]  # Short token for convenience
        self.sessions[session_id] = {
            "created_at": datetime.now().isoformat(),
            "last_active": datetime.now().isoformat(),
            "persona": None,
            "conversation_history": []
        }
        self.save_sessions()
        return session_id
    
    def get_session(self, session_id: str) -> Optional[Dict]:
        """Get session data by ID"""
        if session_id in self.sessions:
            # Update last active
            self.sessions[session_id]["last_active"] = datetime.now().isoformat()
            self.save_sessions()
            return self.sessions[session_id]
        return None
    
    def update_session(self, session_id: str, persona: str = None, conversation_history: list = None):
        """Update session data"""
        if session_id in self.sessions:
            if persona:
                self.sessions[session_id]["persona"] = persona
            if conversation_history is not None:
                self.sessions[session_id]["conversation_history"] = conversation_history
            
            self.sessions[session_id]["last_active"] = datetime.now().isoformat()
            self.save_sessions()
    
    def cleanup_old_sessions(self, days_old: int = 7):
        """Remove sessions older than specified days"""
        cutoff_date = datetime.now() - timedelta(days=days_old)
        expired_sessions = []
        
        for session_id, session_data in self.sessions.items():
            last_active = datetime.fromisoformat(session_data["last_active"])
            if last_active < cutoff_date:
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            del self.sessions[session_id]
        
        if expired_sessions:
            self.save_sessions()
        
        return len(expired_sessions)
