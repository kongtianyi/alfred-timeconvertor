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
### Basic Features
1. get timestamp and local datetime for now
 ![image](https://user-images.githubusercontent.com/15275771/206884336-35a9e96f-1940-45f2-adea-f56f7e7a7584.png)
2. convert timestamp to local datetime
 ![image](https://user-images.githubusercontent.com/15275771/206884345-a135360d-2351-4078-ba8a-24ded9022a05.png)
3. convert local datetime to timestamp
 ![image](https://user-images.githubusercontent.com/15275771/206884355-b9f01e59-ea5e-43aa-979a-a3e797aa725d.png)
### I18N Features
1. get timestamp certain timezones' datetime for now
 ![image](https://user-images.githubusercontent.com/15275771/206884128-b08d2201-e306-4543-b8f1-a4811f913f4f.png)
2. convert timestamp to certain timezones' datetime 
 ![image](https://user-images.githubusercontent.com/15275771/206884158-114308c2-d051-4083-81e1-0ad7c006b37e.png)
3. convert local timezone datetime to other timezones' datetime
 ![image](https://user-images.githubusercontent.com/15275771/206884186-1f0bae6a-1357-4bb7-b74b-4c4cc7eed014.png)
4. convert certain timezone datetime to timestamp
 ![image](https://user-images.githubusercontent.com/15275771/206884209-a2d9af55-80d6-40ae-a4f0-aaa046399766.png)
5. convert certain timezone datetime to other timezones' datetime
 ![image](https://user-images.githubusercontent.com/15275771/206884252-24e22482-8700-4327-8d33-f9795df90262.png)

## Appendix

* windows version: https://github.com/kongtianyi/timestampforwox
* refer: https://github.com/xindoo/timestamp-workflow
