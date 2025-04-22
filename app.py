from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import paramiko
import psutil


app = Flask(__name__)
app.secret_key = 'supersecretkey'

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
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error=client)
    
    return render_template('login.html')

# Dashboard Route
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

# Get running processes
@app.route('/processes')
def processes():
    processes = [proc.info for proc in psutil.process_iter(['pid', 'name'])]
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
    return jsonify({'cpu': cpu, 'memory': memory, 'disk': disk, 'network': network})

if __name__ == '__main__':
    app.run(debug=True)
