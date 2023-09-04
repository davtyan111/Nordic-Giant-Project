#!/bin/bash

# Command to perform a rolling restart of pods in a Deployment
kubectl_command="kubectl rollout restart deployment/laravel-deployment -n laravel"

# Retrieve AWS access key ID, secret access key, region, and EKS cluster name from environment variables
access_key_id="$access_key_id"
secret_access_key="$secret_access_key"
aws_region="$AWS_REGION"
eks_cluster_name="$EKS_CLUSTER_NAME"

# Create an AWS EKS client
eks_client="aws eks --region $aws_region"

try {
  # Get the EKS cluster configuration
  cluster_info=$(eks_client describe-cluster --name "$eks_cluster_name")
  cluster_certificate_data=$(echo "$cluster_info" | jq -r '.cluster.certificateAuthority.data')
  cluster_endpoint=$(echo "$cluster_info" | jq -r '.cluster.endpoint')

  # Save the cluster configuration to a kubeconfig file
  kubeconfig_file_path="/tmp/kubeconfig.yaml"
  echo "apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: $cluster_certificate_data
    server: $cluster_endpoint
  name: kubernetes
contexts:
- context:
    cluster: kubernetes
    user: eks
  name: eks
current-context: eks
kind: Config
preferences: {}
users:
- name: eks
  user:
    exec:
      apiVersion: client.authentication.k8s.io/v1
      args:
      - eks
      - get-token
      - --cluster-name
      - $eks_cluster_name
      command: aws
      env: null
      interactiveMode: "Never"" > "$kubeconfig_file_path"

  # Execute the kubectl command using the kubeconfig file
  "$kubectl_command" --kubeconfig "$kubeconfig_file_path"
  echo "Command executed successfully."
} catch {
  e=$(echo $?)
  echo "Error executing kubectl command: $e"
} finally {
  echo "Script completed."
}
