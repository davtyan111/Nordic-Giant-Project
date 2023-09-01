import subprocess
import boto3

# Замените на свои учетные данные AWS
region_name = "us-east-2"
eks_cluster_name = 'clusters'

# Команда для выполнения перезапуска подов в Deployment
kubectl_command = "kubectl rollout restart deployment/laravel-deployment -n laravel"

# Создаем клиент EKS
eks_client = boto3.client(
    'eks',
    access_key_id_id=access_key_id,
    aws_secret_access_key=secret_access_key,
    region_name=region_name
)

try:
    # Получаем конфигурацию кластера EKS
    cluster_info = eks_client.describe_cluster(name=eks_cluster_name)
    cluster_certificate_data = cluster_info['cluster']['certificateAuthority']['data']
    cluster_endpoint = cluster_info['cluster']['endpoint']

    # Сохраняем конфигурацию кластера в файле kubeconfig
    kubeconfig_file_path = '/tmp/kubeconfig.yaml'
    with open(kubeconfig_file_path, 'w') as kubeconfig_file:
        kubeconfig_file.write(f"""apiVersion: v1
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
      apiVersion: client.authentication.k8s.io/v1  # Версия API
      args:
      - eks
      - get-token
      - --cluster-name
      - {eks_cluster_name}
      command: aws
      env: null
      interactiveMode: "Never"  # Изменено значение на "Never"
""")
    # Выполняем команду kubectl с использованием kubeconfig файла
    subprocess.run(f"{kubectl_command} --kubeconfig {kubeconfig_file_path}", shell=True, check=True, text=True)
    print("Команда успешно выполнена.")
except subprocess.CalledProcessError as e:
    print("Ошибка при выполнении команды kubectl:", e)
except Exception as e:
    print("Произошла ошибка:", e)
