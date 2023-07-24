import docker

def lambda_handler(event, context):
    # Replace these with your Docker Hub credentials
    docker_hub_username = 'davtyan111'
    docker_hub_password = 'rrafo1209'

    # Docker Hub repository details
    docker_hub_repository = 'davtyan111/your_repository_name'
    dockerfile_path = 'lambda_aws_docker_nordic'

    # Authenticate with Docker Hub
    client = docker.from_env()
    client.login(username=docker_hub_username, password=docker_hub_password)

    try:
        # Build the Docker image
        image, build_logs = client.images.build(path=dockerfile_path, tag=docker_hub_repository)

        # Push the image to Docker Hub
        for line in client.images.push(repository=docker_hub_repository, stream=True, decode=True):
            print(line)  # Optional: Print the push logs for visibility

        return {
            'statusCode': 200,
            'body': 'Image successfully built and pushed to Docker Hub.'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error: {str(e)}'
        }
