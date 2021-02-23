# Automated downloading of Raspberry Pi Pico firmware files

An automated script to find and download new Raspberry Pi Pico firmware files from https://micropython.org/download/rp2-pico/ via a manual or timed/scheduled process.

## Simple to run:

```
$ python3 ./fetch_pico_firmware.py 
rp2-pico-20210222-unstable-v1.14-80-g75db0b907.uf2: downloading from https://micropython.org/resources/firmware/rp2-pico-20210222-unstable-v1.14-80-g75db0b907.uf2
rp2-pico-20210221-unstable-v1.14-74-g1342debb9.uf2: downloading from https://micropython.org/resources/firmware/rp2-pico-20210221-unstable-v1.14-74-g1342debb9.uf2
rp2-pico-20210220-unstable-v1.14-72-gd28dbcd6c.uf2: downloading from https://micropython.org/resources/firmware/rp2-pico-20210220-unstable-v1.14-72-gd28dbcd6c.uf2
rp2-pico-20210219-unstable-v1.14-70-g143372ab5.uf2: downloading from https://micropython.org/resources/firmware/rp2-pico-20210219-unstable-v1.14-70-g143372ab5.uf2
rp2-pico-20210202-v1.14.uf2: downloading from https://micropython.org/resources/firmware/rp2-pico-20210202-v1.14.uf2
$
```
The files are time-stamped based on their included date - this is important as you want to really confirm you're using the latest and greatest!
```
$ ls -lt *.uf2
-rw-r--r--  1 martin  martin 497664 Feb 22 00:00 rp2-pico-20210222-unstable-v1.14-80-g75db0b907.uf2
-rw-r--r--  1 martin  martin 497664 Feb 21 00:00 rp2-pico-20210221-unstable-v1.14-74-g1342debb9.uf2
-rw-r--r--  1 martin  martin 497664 Feb 20 00:00 rp2-pico-20210220-unstable-v1.14-72-gd28dbcd6c.uf2
-rw-r--r--  1 martin  martin 497664 Feb 19 00:00 rp2-pico-20210219-unstable-v1.14-70-g143372ab5.uf2
-rw-r--r--  1 martin  martin 497664 Feb  2 00:00 rp2-pico-20210202-v1.14.uf2
$
```
A subsequent run will not download these files again (unless there are new files to be found).
```
$ python3 ./fetch_pico_firmware.py 
rp2-pico-20210222-unstable-v1.14-80-g75db0b907.uf2: already downloaded, hence skipped
rp2-pico-20210221-unstable-v1.14-74-g1342debb9.uf2: already downloaded, hence skipped
rp2-pico-20210220-unstable-v1.14-72-gd28dbcd6c.uf2: already downloaded, hence skipped
rp2-pico-20210219-unstable-v1.14-70-g143372ab5.uf2: already downloaded, hence skipped
rp2-pico-20210202-v1.14.uf2: already downloaded, hence skipped
$ 
```
Over time, by running this occasionally, you will end up with a complete collection of firmwares for running and testing.

## Command line flags

```
$ ./fetch_pico_firmware.py -H
usage: fetch_firmware_rp2 [-H|--help] [-q|--quiet] [-v|--verbose] [-o|--overwrite] [-u|--utc] 
$
```

`-H` - Help message

`-q` - No output during normal operations

`-v` - debug/verbose info

'-o' - overwrite the files 

'-u' - run in UTC timezone

## Install

Grabbing from _github_ is easy. Adjust the folder/directory choice as-needed.

```
$ cd
$ git clone https://github.com/mahtin/fetch_pico_firmware.git
$ cd fetch_pico_firmware
```
The following Python installs are required before running:
```
$ cat requirements.txt 
requests
beautifulsoup4
$

$ pip3 install `cat requirements.txt`
...
$
```

## Automated operations

Throwing something in crontab should be easy to do; however, once the firmware becomes more stable, I recommend checking the website on a less often basis.

Edit your crontab (via the `crontab -e` command) and add the following line:

```
@daily cd $HOME/fetch_pico_firmware && ./fetch_pico_firmware.py -q

```
You can change the path as-needed.

## Notes

As always, open issues or pull requests should you need - Martin

