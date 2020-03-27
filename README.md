4Bill test exercise
===========

## Explanation
[Test task file](4bill_test_task.pdf)

## Setup
Quickly run the project using [docker](https://www.docker.com/) and [docker-compose](https://docs.docker.com/compose/):
```bash
docker-compose up
```

## Configuration

The following environment variables are *optional*:

| Name              | Purpose                                          |
|-------------------|--------------------------------------------------|
| `FLASK_APP`       | The application main file.                       |
| `FLASK_ENV`       | The application environment.                     |
| `DEBUG`           | The application debug mode.                      |
| `TESTING`         | The application test mode.                       |
| `MEMCACHED_HOST`  | The hostname of a memcached server.              |
| `MEMCACHED_PORT`  | The port of a memcached server.                  |