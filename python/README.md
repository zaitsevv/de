# Python Task

Script uses docker to run Postgresql, so to run it you must have docker and docker-compose installed locally

### How to run it

Easiest way is to use default script parameters:

```shell
make build
make default_run
```

Default parameters:
```shell
python src/main.py --rooms-path data/rooms.json \
                   --students-path data/students.json \
                   --output-path . \
                   --output-format json
```

Also, you can run it with your own configuration:

```shell
make build
python src/main.py [OPTIONS...]
```

```text
Options:
  -r, --rooms-path TEXT           Path to file with data about rooms
  -s, --students-path TEXT        Path to file with data about students
  -o, --output-path TEXT          Output file path
  -f, --output-format [json|xml]  Output file format
  --help                          Show help message and exit.
```

After using the script, run

```shell
make stop_services
```

to stop Postgresql container
