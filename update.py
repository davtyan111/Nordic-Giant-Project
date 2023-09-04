import os
import subprocess
import json

# Command to perform a rolling restart of pods in a Deployment
kubectl_command = "kubectl rollout restart deployment/laravel-deployment -n laravel"

# Retrieve AWS access key ID, secret access key, region, and EKS cluster name from environment variables
access_key_id = os.environ.get("access_key_id")
secret_access_key = os.environ.get("secret_access_key")
aws_region = os.environ.get("AWS_REGION")
eks_cluster_name = os.environ.get("EKS_CLUSTER_NAME")

# Function to check for errors
def check_error(return_code):
    if return_code != 0:
        print("Error executing last command. Exiting.")
        exit(1)

# Get the EKS cluster configuration
eks_client_command = ["aws", "eks", "--region", aws_region, "describe-cluster", "--name", eks_cluster_name]
try:
    cluster_info = subprocess.check_output(eks_client_command)
    check_error(0)
except subprocess.CalledProcessError as e:
    check_error(e.returncode)

cluster_info_json = json.loads(cluster_info)
cluster_certificate_data = cluster_info_json["cluster"]["certificateAuthority"]["data"]
cluster_endpoint = cluster_info_json["cluster"]["endpoint"]

# Save the cluster configuration to a kubeconfig file
kubeconfig_file_path = "/tmp/kubeconfig.yaml"
kubeconfig_data = f"""apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: {cluster_certificate_data}
    server: {cluster_endpoint}
  name: kubernetes
contexts:
- context:
    cluster: kubernetes
    user: eks
  name: eks
current-context: eks
kind: Config
preferences: {{}}
users:
- name: eks
  user:
    exec:
      apiVersion: client.authentication.k8s.io/v1
      args:
      - eks
      - get-token
      - --cluster-name
      - {eks_cluster_name}
      command: aws
      env: null
      interactiveMode: "Never"
"""

try:
    with open(kubeconfig_file_path, "w") as kubeconfig_file:
        kubeconfig_file.write(kubeconfig_data)
except Exception as e:
    check_error(1)

# Execute the kubectl command using the kubeconfig file
kubectl_command = ["kubectl", "--kubeconfig", kubeconfig_file_path] + kubectl_command.split()
try:
    subprocess.check_call(kubectl_command)
    check_error(0)
except subprocess.CalledProcessError as e:
    check_error(e.returncode)

print("Command executed successfully.")
print("Script completed.")
