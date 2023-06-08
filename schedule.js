/* Add a date and a time selector to the page. */
function addDateTime() {
    var dateTime = document.createElement('input');
    dateTime.setAttribute('type', 'datetime-local');
    dateTime.setAttribute('name', 'datetime');
    dateTime.setAttribute('id', 'datetime');
    document.getElementById('datetime-container').appendChild(dateTime);
}
addDateTime();

/* Add a submit button to the page. */
function addSubmit() {
    var submit = document.createElement('input');
    submit.setAttribute('type', 'submit');
    submit.setAttribute('value', 'Submit');
    document.getElementById('datetime-container').appendChild(submit);
}
addSubmit();

/* Add a reset button to the page. */
function addReset() {
    var reset = document.createElement('input');
    reset.setAttribute('type', 'reset');
    reset.setAttribute('value', 'Reset');
    document.getElementById('datetime-container').appendChild(reset);
}
addReset();

/* Add a Timezone Selector to the page. */
function addTimezone() {
    var timezone = document.createElement('select');
    timezone.setAttribute('name', 'timezone');
    timezone.setAttribute('id', 'timezone');
    var options = ['Pacific/Auckland', 'Australia/Sydney', 'Europe/London', 'America/New_York', 'America/Chicago', 'America/Denver', 'America/Los_Angeles', 'America/Anchorage', 'Pacific/Honolulu'];
    for (var i = 0; i < options.length; i++) {
        var option = document.createElement('option');
        option.setAttribute('value', options[i]);
        option.innerHTML = options[i];
        timezone.appendChild(option);
    }
    document.getElementById('datetime-container').appendChild(timezone);
}  
addTimezone();

/* create a list of all the timezones */
function getTimezones() {
    var timezones = [];
    var options = document.getElementsByTagName('option');
    for (var i = 0; i < options.length; i++) {
        timezones.push(options[i].value);
    }
    return timezones;
}
var timezones = getTimezones();


/* Add a hidden field to store utc datetime */
function addHidden() {
    var hidden = document.createElement('input');
    hidden.setAttribute('type', 'hidden');
    hidden.setAttribute('name', 'utc');
    hidden.setAttribute('id', 'utc');
    document.getElementById('datetime-container').appendChild(hidden);
}
addHidden();


/* convert the datetime input to the same datetime in the timezone selected using plain javascript */
function convertDateTime() {
    var datetime = document.getElementById('datetime').value;
    var timezone = document.getElementById('timezone').value;

    if (datetime) {
        var utc = new Date(datetime).getTime() + (new Date(datetime).getTimezoneOffset() * 60000);
        var utcDateTime = new Date(utc);
        var utcDateTimeString = utcDateTime.toISOString().slice(0, -1);
        var utcDateTimeString = utcDateTimeString.replace('T', ' ');
        var utcDateTimeString = utcDateTimeString.replace(/-/g, '/');
        var utcDateTimeString = utcDateTimeString.replace(/:/g, ':');
        var utcDateTimeString = utcDateTimeString.replace(/\.\d{3}/, '');
        var utcDateTimeString = utcDateTimeString + ' ' + timezone;
        console.log(utcDateTimeString);
    }
}


/* store convertDateTime in a hidden field */
function storeDateTime() {
    var utcDateTimeString = convertDateTime();
    document.getElementById('utc').value = utcDateTimeString;
}


/* Create a table with a row for each timezone and a column to display the time. */
function createTable() {
    var table = document.createElement('table');
    table.setAttribute('id', 'table');
    var timezones = getTimezones();
    for (var i = 0; i < timezones.length; i++) {
        var row = document.createElement('tr');
        var timezone = timezones[i];
        var column = document.createElement('td');
        column.innerHTML = getTime(timezone);
        row.appendChild(column);
        table.appendChild(row);
    }
    document.getElementById('table-container').appendChild(table);
}
createTable();

/* Add a td to each row of the table with the timezone name in it */
function addTimezoneNames() {
    var timezones = getTimezones();
    var table = document.getElementById('table');
    for (var i = 0; i < timezones.length; i++) {
        var row = table.rows[i];
        var column = document.createElement('td');
        column.innerHTML = timezones[i];
        row.appendChild(column);
    }
}
addTimezoneNames();


/* convert UTC javascript date object back 


/* Create a getTime function that returns the utc datetime in the specified timezone. */
function getTime(timezone) {
    var utc = new Date(document.getElementById('utc').value);
    var offset = new Date(utc.toLocaleString('en-US', { timeZone: timezone }));
    var time = offset.toLocaleTimeString();
    return time;
}


/* Create a function that updates the time in the table. */
function updateTime() {
    var timezones = getTimezones();
    for (var i = 0; i < timezones.length; i++) {
        var time = getTime(timezones[i]);
        document.getElementById('table').rows[i].cells[0].innerHTML = time;
    }
}

/* When the timezone changes update the time in the table. */
document.getElementById('timezone').addEventListener('change', updateTime);
updateTime();


/* When the datetime changes update the time in the table. */
document.getElementById('datetime').addEventListener('change', updateTime);
updateTime();
