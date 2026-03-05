# MySQL Dockerized Backup

A Docker-based tool for backing up MySQL databases with automatic rotation and compression.

## Features

- Backup MySQL databases to compressed `.tar.gz` files
- Automatic cleanup of old backups based on configured retention days
- REST API endpoint to trigger backups
- Configurable via environment variables

## Quick Start

```bash
# Configure environment variables
cp .env.example .env
# Edit .env with your database credentials

# Build and run with Docker Compose
docker-compose up -d
```

## Configuration

Configure the following environment variables:

| Variable | Description | Required |
|----------|-------------|----------|
| `DB_HOST` | MySQL server hostname | Yes |
| `DB_USER` | MySQL username | Yes |
| `DB_PASSWORD` | MySQL password | Yes |
| `DAYS` | Number of days to keep backups | Yes |

## Database Selection

Edit the `backup/names` file to specify which databases to backup. Add one database name per line:

```
database1
database2
database3
```

## Usage

### Trigger a Backup

Make a GET request to the backup endpoint:

```bash
curl http://localhost:5000/backup
```

The response will be `"Backup finished"` when complete.

### Backup Output

Backups are saved to the `/app/backup` volume (mapped to `./backup` by default in docker-compose).

Format: `{database_name}{date}.tar.gz`

Example: `haberes20260305.tar.gz`

### Automatic Cleanup

Backups older than the configured `DAYS` value are automatically deleted after each backup run.

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── app.py          # Flask application
│   └── task.py         # Backup logic
├── backup/
│   └── names           # List of databases to backup
├── .env.example        # Environment variables template
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## License

See [LICENSE](LICENSE) file.
