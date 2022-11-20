# Cookie Cutter Web
## Getting Started

```bash
$ make server.install      # Install the pip dependencies on the docker container
$ make server.start        # Run the container containing your local python server
```

## Usage 

```
POST /api/generator/cutter

multipart/form-data
file=<image>.png
```

## Development

To develop locally, here are your two options:

```bash
$ make server.start           # Create the containers containing your python server in your terminal
$ make server.daemon          # Create the containers containing your python server as a daemon
```

The containers will reload by themselves as your source code is changed.

## Testing

```bash
$ make test
```
