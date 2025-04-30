from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import paramiko
import psutil

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# SSH client storage
ssh_clients = {}

# Function to establish SSH connection
def connect_ssh(username, ip, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(ip, username=username, password=password)
        return client
    except Exception as e:
        return str(e)

# Login Route
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        ip = request.form['ip']
        password = request.form['password']
        client = connect_ssh(username, ip, password)
        
        if isinstance(client, paramiko.SSHClient):
            session['username'] = username
            session['ip'] = ip
            session['password'] = password
            ssh_clients[username] = client
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error=client)
    
    return render_template('login.html')

# Logout Route
@app.route('/logout')
def logout():
    if 'username' in session:
        username = session['username']
        if username in ssh_clients:
            ssh_clients[username].close()
            del ssh_clients[username]
    session.clear()
    return redirect(url_for('login'))

# Dashboard Route
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

# Terminal Route
@app.route('/terminal')
def terminal():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('terminal.html')

# Execute Command Route
@app.route('/execute_command', methods=['POST'])
def execute_command():
    if 'username' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    command = request.json.get('command')
    username = session['username']
    
    if username not in ssh_clients:
        return jsonify({'error': 'SSH connection lost'}), 500
    
    try:
        stdin, stdout, stderr = ssh_clients[username].exec_command(command)
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        return jsonify({'output': output + error})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Processes Route
@app.route('/processes_page')
def processes_page():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('processes.html')

# Get running processes with detailed info
@app.route('/processes')
def processes():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            proc_info = proc.info
            # Update CPU and memory percentages
            proc_info['cpu_percent'] = proc.cpu_percent()
            proc_info['memory_percent'] = proc.memory_percent()
            processes.append(proc_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return jsonify(processes)

# Kill a process
@app.route('/kill_process/<int:pid>', methods=['POST'])
def kill_process(pid):
    try:
        p = psutil.Process(pid)
        p.terminate()
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# Get system resource usage
@app.route('/resource_usage')
def resource_usage():
    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    network = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
    return jsonify({
        'cpu': cpu,
        'memory': memory,
        'disk': disk,
        'network': network
    })

if __name__ == '__main__':
    app.run(debug=True)
