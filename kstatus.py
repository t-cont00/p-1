pip install flask kubernetes




from flask import Flask, render_template, jsonify
from kubernetes import client, config

app = Flask(__name__)

# Load kubeconfig (or use in-cluster config if deployed inside cluster)
try:
    config.load_kube_config()  # for local testing
except:
    config.load_incluster_config()  # for deployed pod inside k8s

v1 = client.CoreV1Api()


def get_namespace_status():
    namespaces = v1.list_namespace().items
    data = []

    for ns in namespaces:
        ns_name = ns.metadata.name
        pods = v1.list_namespaced_pod(ns_name).items
        pod_list = []
        all_running = True

        for pod in pods:
            status = pod.status.phase
            pod_list.append({"name": pod.metadata.name, "status": status})
            if status != "Running":
                all_running = False

        data.append({
            "namespace": ns_name,
            "status": "all_running" if all_running else "not_running",
            "pods": pod_list
        })

    return data


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/namespaces')
def namespaces_api():
    data = get_namespace_status()
    return jsonify(data)


@app.route('/api/namespace/<ns_name>/pods')
def pods_api(ns_name):
    pods = v1.list_namespaced_pod(ns_name).items
    pod_list = [{"name": pod.metadata.name, "status": pod.status.phase} for pod in pods]
    return jsonify(pod_list)


if __name__ == "__main__":
    app.run(debug=True)






templates/index.html




<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>K8s Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; }
        .namespace-box { 
            display: inline-block; 
            width: 200px; 
            height: 100px; 
            margin: 10px; 
            padding: 10px; 
            color: white; 
            cursor: pointer; 
            text-align: center; 
            vertical-align: top;
            border-radius: 8px;
        }
        .all_running { background-color: green; }
        .not_running { background-color: red; }
        table { border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
    </style>
</head>
<body>
    <h1>Kubernetes Dashboard</h1>
    <div id="namespaces"></div>
    <div id="pod-details"></div>

    <script>
        async function fetchNamespaces() {
            const res = await fetch('/api/namespaces');
            const data = await res.json();

            const container = document.getElementById('namespaces');
            container.innerHTML = '';
            data.forEach(ns => {
                const box = document.createElement('div');
                box.className = 'namespace-box ' + ns.status;
                box.textContent = ns.namespace;
                box.onclick = () => fetchPods(ns.namespace);
                container.appendChild(box);
            });
        }

        async function fetchPods(ns_name) {
            const res = await fetch(`/api/namespace/${ns_name}/pods`);
            const pods = await res.json();

            const details = document.getElementById('pod-details');
            let html = `<h2>Pods in ${ns_name}</h2>`;
            html += '<table><tr><th>Pod Name</th><th>Status</th></tr>';
            pods.forEach(p => {
                html += `<tr><td>${p.name}</td><td>${p.status}</td></tr>`;
            });
            html += '</table>';
            details.innerHTML = html;
        }

        // Auto-refresh every 60 seconds
        fetchNamespaces();
        setInterval(fetchNamespaces, 60000);
    </script>
</body>
</html>

