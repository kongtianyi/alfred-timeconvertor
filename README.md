# alfred-timeconvertor
An alfred workflow that do time convert, including i18n features.

Workflow file is in the repo's root derictory, named `Time Convertor.alfredworkflow`. You can just download it on your mac and double click to install.

## Input Format
```
ts (now|<timestamp>|<datetime>[#<timezone>]) [<timezone>]...
# timestamp support second and milisecond
# datetime's format is yyyy-MM-dd hh:mm:ss
# timezone's format is utc[\+|\-][0-9]+(utc, utc8, utc-12 etc.)
```

## Examples
1. get local timestamp and datetime for now
 ![image](https://user-images.githubusercontent.com/15275771/206860949-a660ca09-b430-4286-b646-82d93b29268a.png)
2. convert timestamp to local datetime
 ![image](https://user-images.githubusercontent.com/15275771/206861015-c44dfd97-9cc3-419b-84c7-f63d81855db3.png)
3. convert local datetime to timestamp
 ![image](https://user-images.githubusercontent.com/15275771/206861044-53d960c9-16ac-4a4e-9d82-79249ee89f71.png)

## Appendix

* windows version: https://github.com/kongtianyi/timestampforwox
* refer: https://github.com/xindoo/timestamp-workflow
