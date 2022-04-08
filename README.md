# WebHDFS-Commander
HDFS commander on Python 3

![_-code-_-written-by-myself](https://user-images.githubusercontent.com/31628014/162436697-a87ec5fe-980c-4377-931f-f6f2e3eade8c.svg)

[![made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

## OS Compatibility

[![Linux](https://svgshare.com/i/Zhy.svg)](https://ru.wikipedia.org/wiki/Linux)
[![Windows](https://svgshare.com/i/ZhY.svg)](https://ru.wikipedia.org/wiki/Windows)
[![macOS](https://svgshare.com/i/ZjP.svg)](https://ru.wikipedia.org/wiki/MacOS)

## Commands

If you are in program, connection is successful. To successfully connect use `$ > python3 ./{hdfscommander.py} {ip} 50070 {username}`

### Available commands:

- ? or help — Help page

- mkdir {dirname} {permissions in OCT} — Creating a HDFS directory in current path.

Example: `$ > mkdir newdirectory 755`

- put {localfile} — Upload file to HDFS current path.

Example: `$ > put testfile.txt`

- get {remotefile} — Download file to local path of your machine.

Example: `$ > get testfile.hdp`

- append {localfile} {remotefile} — Append (concat) local file with remote file.

Example: `$ > append test01 test02`

- delete {remotefile} — Recursively delete file or directory on HDFS.

Example: `$ > delete junkfolder`

- ls — List status of current path on HDFS.

Example: `$ > ls`

- cd \[., .., {directory}, \*{path}] — Change directory of HDFS path recognition.

  - Example: `$ > cd .`                     

  - `.`        —  _Is remain you into your current path._

  - Example: `$ > cd ..`                    

  - `..`       —  _Is moving you on level high._

  - Example: `$ > cd intfolder`            

  - `{dir}`    —  _Is moving you to directory._

  - Example: `$ > cd */user/wow`          

  - `*{path}`  —  _Is moving you to absolute path._

- lls — List status of local path.

Example: `$ > lls`

- lcd \[., .., {directory}, \*{path}] — Change directory of local machine.

Example check out on `cd` command. All is the same.

WARN! LOCAL and HDFS paths are global variables. For perfect working after changing directories (HDFS or LOCAL) type LS or LLS commands for checking out paths to correct values.

# Hadoop

[![Hadoop](https://user-images.githubusercontent.com/31628014/156457088-d77db39d-5c04-4954-b898-c303de58792e.png)](https://hadoop.apache.org/)

## What is HDFS?
**HDFS** — Hadoop Distributed File System is a distributed file system designed to run on commodity hardware. It has many similarities with existing distributed file systems. However, the differences from other distributed file systems are significant. HDFS is highly fault-tolerant and is designed to be deployed on low-cost hardware. HDFS provides high throughput access to application data and is suitable for applications that have large data sets. HDFS relaxes a few POSIX requirements to enable streaming access to file system data. HDFS was originally built as infrastructure for the Apache Nutch web search engine project. HDFS is now an Apache Hadoop subproject. 
The project URL is https://hadoop.apache.org/hdfs/

## Hadoop architecture
https://hadoop.apache.org/docs/r1.2.1/hdfs_design.html

## WebHDFS REST API
The HTTP REST API supports the complete FileSystem interface for HDFS.

https://hadoop.apache.org/docs/r1.2.1/webhdfs.html


