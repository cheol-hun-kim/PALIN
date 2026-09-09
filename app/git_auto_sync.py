"""
PALIN OS Git Auto Sync Module
Automatically commits and pushes modified / added files to GitHub repository.
"""
import subprocess
import os
from datetime import datetime

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def auto_push_to_github(commit_msg: str = None) -> dict:
    if not commit_msg:
        commit_msg = f"Auto-sync: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    try:
        # 1. git add .
        subprocess.run(['git', 'add', '.'], cwd=REPO_DIR, check=True)
        
        # 2. Check if there are changes
        status = subprocess.run(['git', 'status', '--porcelain'], cwd=REPO_DIR, capture_output=True, text=True)
        if not status.stdout.strip():
            return {'status': 'no_changes', 'message': 'No new changes to commit.'}
            
        # 3. git commit
        subprocess.run(['git', 'commit', '-m', commit_msg], cwd=REPO_DIR, check=True)
        
        # 4. git push
        push_res = subprocess.run(['git', 'push', 'origin', 'main'], cwd=REPO_DIR, capture_output=True, text=True)
        if push_res.returncode == 0:
            return {'status': 'success', 'message': 'Pushed to GitHub successfully.'}
        else:
            return {'status': 'error', 'message': push_res.stderr}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

if __name__ == '__main__':
    result = auto_push_to_github('feat: Add git auto-sync engine')
    print(result)
