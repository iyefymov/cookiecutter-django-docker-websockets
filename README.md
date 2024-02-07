# cookiecutter.django_channels_docker

This is a Dockerized Django application that uses WebSockets for real-time communication.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Docker
- Docker Compose

### Installation

1. Clone the repository
```git clone https://github.com/yourusername/{{cookiecutter.project_slug}}.git```

2. Navigate to the project directory
```cd cookiecutter/django_channels_docker```

3. Build the Docker image
```docker-compose build```

4. Run the Docker container
```docker-compose up```

Now, your Django application should be running at `localhost:8000`.

## Usage

This project includes a simple chat application. To use it, navigate to `localhost:8000/chat/`.


## License

This project is licensed under the MIT License - see the `LICENSE.md` file for details