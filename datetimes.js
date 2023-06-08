/* a plain javascript class that provides html elements to set a data and time with a timezone
 * the class will return the date and time in the specified timezone.
 * the class will retrun the date and time in a pre set list of timezones.
 */
class Timezoned {
    /*
    * @param {string} timezone - the timezone to use
    * @param {string} date - the date to use
    */
    constructor(timezone, date) {
        this.prefix = "timezone_"
        this.id = this.createId(this.prefix)
        this.timezone = timezone;
        this.timezones = this.getTimezones();
        this.date = date;
        this.date_utc = this.convertToTimeZone(date,this.timezone);
    }

    /* create a unique html element id with the provided prefix */
    createId(prefix) {
        return prefix + '_' + Math.random().toString(36).substr(2, 9);
    }
    getDate() {
        return this.date;
    }

    /*
    * @param {string} date - the date to use
    * 
    */
    setDate(date) {
        this.date = date;
    }

    getUTCDate() {
        return this.utc_date;
    }

    setUTCDate() {
        this.date_utc = this.convertToTimeZone(this.date,this.timezone);
    }

    /*
     * @param {string} timezone - the timezone to use
     * @param {string} date - the date to use
     */
    getTimezone() {
        return this.timezone;
    }

    /*
     * @param {string} timezone - the timezone to use
     */
    setTimezone(timezone) {
        this.timezone = timezone;
    }

    /*
     * @param {string} timezone - the timezone to use
     * @param {string} date - the date to use
     * 
     * create a timezone list including the following
     * Pacific/Auckland, Australia/Sydney, America/Huston, America/Los_Angeles, America/New_York, Europe/London
     */
    getTimezones() {
        return ["Pacific/Auckland", "Australia/Sydney", "America/Los_Angeles", "America/New_York", "Europe/London"];
    }

    /*
     * @param {string} timeZones - the timezones to use
     */
    setTimezones(timezones) {
        this.timezones = timezones;
    }

    /* convert the provided datetime object to UTC /*
     * @param {string} date - the date to use
     */
    convertToUTC(date) {
        var utc_date = new Date(date);
        utc_date.setMinutes(utc_date.getMinutes() - utc_date.getTimezoneOffset());
        return utc_date;
    }


    convertToTimeZone(date, timezone) {
        return new Date((typeof date === "string" ? new Date(date) : date).toLocaleString("en-US", {timeZone: timezone}));   
    }


    /* given a timezone name, return the index of the timezone in the timezones list */
    getTimezoneIndex(timezone) {
        var index = 0;
        for (var i = 0; i < this.timezones.length; i++) {
            if (this.timezones[i] == timezone) {
                index = i;
                break;
            }
        }
        return index;
    }

    /* retrun a list of timezones with the time from date_utc in each timezone */
    getTimezonesWithTime() {
        var timezones = [];
        var date_utc = this.date_utc;
        for (var i = 0; i < this.timezones.length; i++) {
            var timezone = this.timezones[i];
            var date_timezone = new Date(date_utc);
            date_timezone.setMinutes(date_timezone.getMinutes() + date_utc.getTimezoneOffset());
            date_timezone.setHours(date_timezone.getHours() + date_utc.getTimezoneOffset() / 60);
            date_timezone.setMinutes(date_timezone.getMinutes() - date_utc.getTimezoneOffset());
            date_timezone.setHours(date_timezone.getHours() + date_utc.getTimezoneOffset() / 60);
            timezones.push({
                timezone: timezone,
                time: this.convertToTimeZone(date_utc,timezone)
            });
        }
        return timezones;
    }

    /* return a div to display the current date and time in the timezone */
    htmlTimezoneDiv() {
        var div = document.createElement("div");
        div.id = this.id + '_datetime';
        div.innerHTML = this.date_utc.toLocaleString();
        return div;
    }

    /* update the htmlTimezoneDiv with the current date and time in the timezone */
    updateHtmlTimezoneDiv() {
        var div = document.getElementById(this.id + '_datetime');
        div.innerHTML = this.date_utc.toLocaleString();
    }

    /* return a date and a time selector for the page. */
    htmlDateTimeSelector(label) {
        var div = document.createElement('div');
        if (label) {
            var dateTime_label = document.createElement('label');
            dateTime_label.setAttribute('for', this.id);
            dateTime_label.innerHTML = label;
        }
        var dateTime = document.createElement('input');
        dateTime.setAttribute('type', 'datetime-local');
        dateTime.setAttribute('name', 'datetime');
        dateTime.setAttribute('id', this.id);
        dateTime.addEventListener('change', () => {
            this.date = dateTime.value;
            this.date_utc = this.convertToTimeZone(this.date, this.timezone);
            this.updateHtmlTimezoneDiv();
            this.updateHtmlTimezoneTable();
        });
        div.appendChild(dateTime_label);
        div.appendChild(dateTime);
        return div 
    }

    /* return a timezone selector for the page. */
    htmlTimezoneSelector(label) {
        var div = document.createElement('div');
        if (label) {
            var timezone_label = document.createElement('label');
            timezone_label.setAttribute('for', this.id);
            timezone_label.innerHTML = label
        }
        var timezone = document.createElement('select');
        timezone.setAttribute('name', 'timezone');
        timezone.setAttribute('id', this.id + "_timezone");
        for (var i = 0; i < this.timezones.length; i++) {
            var option = document.createElement('option');
            option.setAttribute('value', this.timezones[i]);
            option.innerHTML = this.timezones[i];
            timezone.appendChild(option);
        }
        timezone.addEventListener('change', () => {
            this.timezone = timezone.value;
            this.setUTCDate();
            this.updateHtmlTimezoneDiv();
            this.updateHtmlTimezoneTable();
        });
        div.appendChild(timezone_label);
        div.appendChild(timezone);
        return div 
    }


    /* return an html table with a row containing the Timezone name and the time in the timezone for each timezone in getTimezonesWithTime */
    htmlTimezoneTable() {
        var table = document.createElement('table');
        table.id = this.id + '_timezone_table';
        var tbody = document.createElement('tbody');
        var row = document.createElement('tr');
        var td = document.createElement('td');
        td.innerHTML = "Timezone";
        row.appendChild(td);
        td = document.createElement('td');
        td.innerHTML = "Time";
        row.appendChild(td);
        tbody.appendChild(row);
        var timezonedata = this.getTimezonesWithTime();
        for (var i = 0; i < timezonedata.length; i++) {
            row = document.createElement('tr');
            td = document.createElement('td');
            td.innerHTML = timezonedata[i].timezone;
            row.appendChild(td);
            td = document.createElement('td');
            td.innerHTML = this.getTimezonesWithTime()[i].time.toLocaleString();
            row.appendChild(td);
            tbody.appendChild(row);
        }
        table.appendChild(tbody);
        return table;
    }

    /* replace the htmlTimezoneTable with new data */
    updateHtmlTimezoneTable() {
        var table = document.getElementById(this.id + '_timezone_table');
        table.parentNode.replaceChild(this.htmlTimezoneTable(), table);
    }


}


/* Function that sets up the page and adds the html elements to the page. */
function setupDatePage() {

    date = new Date();
    show_date = new Timezoned('Pacific/Auckland', date);
    show_date.prefix = "start_"


    /* append start.htmlDateTimeSelector() to the page */
    document.body.appendChild(show_date.htmlDateTimeSelector(label='Date'));
    document.body.appendChild(show_date.htmlTimezoneSelector(label='Timezone'));
    document.body.appendChild(show_date.htmlTimezoneDiv());
    document.body.appendChild(show_date.htmlTimezoneTable());
    
}


document.onload = setupDatePage();
