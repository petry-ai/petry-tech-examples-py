# Load the environment variables from the .env file
export $(cat ./.env)

export DOCKER_BUILDKIT=1

docker build \
--build-arg ENV=${ENV} \
--build-arg OPENAI_API_KEY=${OPENAI_API_KEY} \
--build-arg ALLOWED_HOSTS=${ALLOWED_HOSTS} \
--progress=plain \
--no-cache \
-t petry-tech-examples-py:latest .