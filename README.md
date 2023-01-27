# visilogs
A lightweight and simple set of tools for analysing and archiving logs.

`visilogs` is an opinionated set of tools that makes assumptions about your log files:

- They are in the `jsonl` format (one JSON object per line)
- You backup your log files to an S3-compatible storage service
- You can put all of your log files into the `./logs/fresh` directory
- You can use visidata to analyse your logs

## Getting Started

To take `visilogs` out for a spin download the repo and run the following:

```
$ ./tools/init.py
$ cp ./examples/logs/fresh/* ./logs/fresh/
$ ./tools/analyse.sh
```

This loads a very small demo log file into the fresh logs directory and then analyses them.

## Writing Logs

You need to get your application to write logs in the `jsonl` format.

You then need to get your application to save those logs into the `./logs/fresh` directory. Literally the directory created by the `init.sh` tool, the ones that lives inside the `visilogs` directory. It's in here that the other tools expect your log files to live.

The `fresh` directory is where new logs should be written. There's also an `archive` directory which is where log files from the archive are downloaded to.

## Backing up and Restoring

To backup your logs you'll need to create a `.env` file with some config:

```
BACKUP_ACCESS_KEY=
BACKUP_SECRET_KEY=
BACKUP_ENDPOINT=
BACKUP_BUCKET=
BACKUP_ARCHIVE_AFTER=
```

If you're familiar with S3 then most of these config values should be easy to get a hold of.

The `BACKUP_ARCHIVE_AFTER` value sets the number of days that a log file should sit in the fresh directory before it moves to archive. If you don't set it, the default is 7.

Once this config is ready you can simply run `./tools/backup.py` and any fresh log file that was modified longer ago than your archive after cutoff value will be uploaded to your storage and locally deleted.

It is assumed that you would run this command as a cronjob. In which case you need to make sure you set the `CWD` to the `visilogs` directory so that the tool can find the logs.

To restore archived logs simply run `./tools/restore.py X` where `X` is the number of days of archived logs that you want to download.


## The Tools

To run any of the tools you must have your terminal pointed at the visilogs root directory so you can run the tool using the command `./tools/TOOL`.

The tools assume that the logs live in `./logs/`.

You should absolutely tweak these tools for your own purposes. They're designed to be small tools that are easy to understand and alter.

### `analyse.sh`

Reads in all of the log files in the `./logs/fresh` and `./logs/archive` directories and opens them in visidata. From here you can start to analyse them using all of the options that visidata gives you.

### `backup.py`

Sends any files older than the cutoff to your S3-compatible storage, then deletes the local copy.

### `clean.sh`

Deletes all log files in the `./logs/archive` directory.

### `init.sh`

Initialises visilogs by creating a Python virtual environment and installing the dependecies. visilogs won't work until you've run this tool.

### `play.sh PATH_TO_SESSION_FILE`

Replay a saved visidata session.

### `restore.py NUMBER_OF_DAYS_TO_RESTORE`

Downloads log files from your S3-compatible storage. The number of days argument tells the tool how many days into the past it should go when fetching log files.
