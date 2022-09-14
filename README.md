# Break timer

Contact: David Hunter <dhunter@digitalcreation.co.nz>

Copyright (C) 2022 Digital Creation Ltd 

For license information, see LICENSE.txt

## Features

* Start stop automatically converted to alternative timezones.

* Automatic timer starting when the start time has passed.

* Background can be any image or mp4 movie url (to access local files, the break.html file must be saved and run from your machine "file:///...." ).

* Font colors can be altered to match the background

* The settings can be shared via the "Share URL" which coverts the local start stop time to the local time of the user opening it.



## basic use

### online

https://whojarr.github.io/dcl-break-timers/break.html

### from you pc

The break.html file is full self contained. its is also all contained inside the body of the page.

this can be run local, upstream or the body of the html document pasted anywhere that accepts html, js and css. 


## advanced use

this can be run over https on the local machine or upstream using a python flask app. 

### requires

* python 3.8

* poetry

### run

```shell
poetry install
poetry shell
python ./app.py
```

open browser to https://localhost:5000/