# Vagrant 
Check subdomains to identify which one can contain some interesting stuff.

## Usage
 - File containing a list of subdomain is set with `-d` flag.
 - With `-t` flag you can set a number of threads. Default value is 24.
 - Output can be set in number of ways:
   - With `-o` flag which can get up to 2 arguments: 
   - first one will create file with domains that potentially contain some stuff;
   - second argument will create file with all other alive domains.
   - With `-b` flag which will create 2 files in current directory with the names stored in 'defaults' variable.

## Examples
This one will only show output in terminal.
```
python3 vagrant.py -d domains.list
```
Create one file.
```
python3 vagrant.py -d domains.list -o output
```
Set number of threads and create 2 file to get all alive domains.
```
python3 vagrant.py -d domains.list -o file1 file2 -t 2
```
