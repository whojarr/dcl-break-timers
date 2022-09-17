# Timers

Contact: David Hunter <dhunter@digitalcreation.co.nz>

Copyright (C) 2022 Digital Creation Ltd 

For license information, see [LICENSE.txt](LICENSE.txt)

# Break timer

[break.html](break.html)

## Features

* Start stop automatically converted to alternative timezones.

* Automatic timer starting when the start time has passed.

* Background can be any image or mp4 movie url (to access local files, the break.html file must be saved and run from your machine "file:///...." ).

* Font colors can be altered to match the background

* The settings can be shared via the "Share URL" which coverts the local start stop time to the local time of the user opening it.


The break.html file is full self contained. its is also all contained inside the body of the page.

this can be run local, upstream or the body of the html document pasted anywhere that accepts html, js and css. 


# Date Time

[date.html](date.html)

## Features

* Start Stop date and time

* Background can be any image or mp4 movie url (to access local files, the break.html file must be saved and run from your machine "file:///...." ).

* Font colors can be altered to match the background

* The settings can be shared via the "Share URL" which coverts the local start stop time to the local time of the user opening it.


## basic use

[Online](https://whojarr.github.io/dcl-break-timers/index.html)

[From you PC](/)

## advanced use

this can be run over https on the local machine or upstream using a python flask app. 

### requires

* python 3.8

* poetry

### run
<pre>
poetry install
poetry shell
python ./app.py
</pre>
open browser to [https://localhost:5000/](https://localhost:5000/)