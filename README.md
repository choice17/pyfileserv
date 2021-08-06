# pyfileserv
A simple flask filer serv for embedded linux which support curl binary


## example usage

host side

```
python fileserv.py --host <ip> --port <port>
```


client side

* download file

```
curl -o <filename> http://<ip>:<port>/download?name=<filename>
```

* upload file

```
$ curl -F "data=@<file-location>"" -X POST http://<ip>:<port>/upload?name=<filename>
```

  
