import flet as ft
import datetime
import dateutil.tz as tz
import pytz

# return the label for the timezone specified from timezones in timezone_list
def timezone_label(timezone_name):
    for zone in timezone_list():
        if zone['timezone'] == timezone_name:
            return zone['label']
    return None

def timezone_name(timezone_label):
    for zone in timezone_list():
        if zone['label'] == timezone_label:
            return zone['timezone']
    return None


def timezone_list():
    return [
        {
            "timezone": "Pacific/Auckland",
            "label": "Auckland"
        },
        {
            "timezone": "Australia/Sydney",
            "label": "Sydney"
        },
        {
            "timezone": "Australia/Brisbane",
            "label": "Brisbane"
        },
        {
            "timezone": "Australia/Perth",
            "label": "Perth"
        },
        {
            "timezone": "Europe/London",
            "label": "London"
        },
        {
            "timezone": "America/Los_Angeles",
            "label": "Los Angeles"
        },
        {
            "timezone": "America/Denver",
            "label": "Denver"
        },
        {
            "timezone": "America/Chicago",
            "label": "Chicago"
        },
        {
            "timezone": "America/New_York",
            "label": "New York"
        }
    ]


def datetime_to_timezone(datatime_obj, timezone):
    to_datetime = datatime_obj.astimezone(pytz.timezone(timezone))
    return to_datetime


def datetime_str_to_timezone(datatime_string, timezone):
    fmt = '%Y-%m-%d %H:%M:%S'
    to_timezone = pytz.timezone(timezone)
    dt = datetime.datetime.strptime(datatime_string, fmt)
    to_time = to_timezone.localize(dt)
    return to_time


def datetime_tz_to_tz(datatime_obj, from_timezone, to_timezone):
    from_tz = pytz.timezone(from_timezone)
    to_tz = pytz.timezone(to_timezone)

    if datatime_obj.tzinfo is not None and datatime_obj.tzinfo.utcoffset(datatime_obj) is not None:
        from_datetime_tz = datatime_obj
    else:
        from_datetime_tz = from_tz.localize(datatime_obj)
    result = from_datetime_tz.astimezone(to_tz)

    return result


def appbar(page):
    ab = page.appbar = ft.AppBar(
        leading=ft.Icon(ft.icons.TIMELINE_SHARP),
        title=ft.Text("DCL Timer"),
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[
            ft.IconButton(ft.icons.SLIDESHOW, on_click=lambda _: page.go("/")),
            ft.IconButton(ft.icons.SETTINGS, on_click=lambda _: page.go("/settings"))
        ]
    )
    return ab


def main(page: ft.Page):

    timezone_refs = {}
    date_now_string = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    date_timezone_main_from = None

    def date_selectors_changed(e):
        if date_sel.value and hour_sel_from.value and min_sel_from.value \
            and hour_sel_to.value and min_sel_to.value and timezone_sel.value:

            # Selected Timezone
            tz_label = timezone_label(timezone_sel.value)

            # Datetime string from Selected from fields 0000-00-00 00:00:00 converted to datetime object and date and time values
            datetime_from_string = f'{date_sel.value} {hour_sel_from.value}:{min_sel_from.value}:00'
            datetime_from_tz = datetime_str_to_timezone(datetime_from_string, timezone_sel.value)
            datetime_from = datetime.datetime.strptime(datetime_from_string, '%Y-%m-%d %H:%M:%S')
            date_from_display = datetime_from_tz.strftime('%Y-%m-%d')
            time_from_display = datetime_from_tz.strftime('%H:%M')
            date_timezone_main_from = datetime_from_tz

            # Datetime string from Selected to fields 0000-00-00 00:00:00 converted to datetime object and time value
            datetime_to_string = f'{date_sel.value} {hour_sel_to.value}:{min_sel_to.value}:00'
            datetime_to_tz = datetime_str_to_timezone(datetime_to_string, timezone_sel.value)
            datetime_to = datetime.datetime.strptime(datetime_to_string, '%Y-%m-%d %H:%M:%S')
            time_to_display = datetime_to.strftime('%H:%M')

            # display string 0000-00-00 00:00-00:00 Timzonename
            datetime_display_string = f'{date_from_display} {time_from_display}-{time_to_display} {tz_label}'

            # Update settings page
            datetime_display.value = datetime_display_string
            # enable timezone selectors and update times displayed in the table
            timezones_update(datetime_from_obj=datetime_from, datetime_to_obj=datetime_to, from_timezone=timezone_sel.value)
            
            # Update main page
            date_display_field.value = datetime_display_string
            description_display_field.value = description_field.value


            page.update()

    def page_resize(e):
        page.update()


    def timezone_enabled(e):
        results = []
        for entry in timezone_refs:
            if timezone_refs[entry].cells[0].content.value == True:
                results.append({
                    "timezone_label": timezone_refs[entry].cells[0].content.label,
                    "datetime_from": timezone_refs[entry].cells[1].content.value,
                    "datetime_to": timezone_refs[entry].cells[2].content.value
                })

        new_table = timezones_selected_display(results)
        timezones_selected_display_table.rows = new_table.rows

        page.update()

    # main page
    def background_image():
        return ft.Image(
            src=f"https://img.freepik.com/free-vector/watercolor-abstract-purple-background_23-2149120778.jpg",
            width=page.window_width,
            height=page.window_height,
            fit=ft.ImageFit.COVER
        )

    def description_display():
        return ft.Text(
            style=ft.TextThemeStyle.DISPLAY_LARGE,
            value='Description',
            text_align=ft.TextAlign.CENTER,
            width=800
        )

    def date_display():
        return ft.Text(
            style=ft.TextThemeStyle.DISPLAY_MEDIUM,
            value='0000-00-00 00:00 to 00:00 UTC',
            text_align=ft.TextAlign.CENTER,
            width=800
        )

    def timezones_selected_display(data):
        timezone_rows = []
        for zone in data:
            timezone_rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.Text(
                                style=ft.TextThemeStyle.DISPLAY_MEDIUM,
                                value=zone['timezone_label']
                            )
                        ),
                        ft.DataCell(
                            ft.Text(
                                style=ft.TextThemeStyle.DISPLAY_MEDIUM,
                                value=zone['datetime_from']
                            )
                        ),
                        ft.DataCell(
                            ft.Text(
                                style=ft.TextThemeStyle.DISPLAY_MEDIUM,
                                value=zone['datetime_to']
                            )
                        )
                    ],

                )
            )

        return ft.DataTable(
            columns=[
                ft.DataColumn(
                    ft.Text(
                        style=ft.TextThemeStyle.DISPLAY_SMALL,
                        value=""
                    )
                ),
                ft.DataColumn(
                    ft.Text(
                        style=ft.TextThemeStyle.DISPLAY_SMALL,
                        value=""
                    )
                ),
                ft.DataColumn(
                    ft.Text(
                        style=ft.TextThemeStyle.DISPLAY_SMALL,
                        value=""
                    )
                )
            ],
            heading_row_height=1,
            rows=timezone_rows,
            width=1200,
            data_row_height=70
        )


    # settings page

    def date_selector():
        return ft.TextField(
            label="Date",
            value='2022-12-30',
            width=150,
            on_change=date_selectors_changed
        )

    def hour_selector():
        hour_options = []
        for i in range(0, 24):
            string = str(i)
            if i <= 9:
                string = f'0{i}'
            hour_options.append(ft.dropdown.Option(string))

        return ft.Dropdown(
            label='Hr',
            width=75,
            options=hour_options,
            on_change=date_selectors_changed
        )

    def minute_selector():
        minute_options = []
        for i in range(0, 60):
            string = str(i)
            if i <= 9:
                string = f'0{i}'
            minute_options.append(ft.dropdown.Option(string))

        return ft.Dropdown(
            label='Mn',
            width=75,
            options=minute_options,
            on_change=date_selectors_changed
        )

    def timezone_selector():
        timezone_options = []
        timezones = timezone_list()
        for zone in timezones:
            key = zone['timezone']
            label = zone['label']
            timezone_options.append(ft.dropdown.Option(key=key, text=label))
        return ft.Dropdown(
            label='Timezone',
            width=250,
            options=timezone_options,
            on_change=date_selectors_changed
        )

    def description_input():
        return ft.TextField(label="Description", on_blur=date_selectors_changed)

    def datetime_display_text():
        return ft.Text(date_now_string)


    def timezones_update(datetime_from_obj=None, datetime_to_obj=None, from_timezone=None, format='split'):

        if not from_timezone:
            from_timezone = 'UTC'

        timezones = timezone_list()
        for zone in timezones:
            datetime_from_tz = datetime_tz_to_tz(datetime_from_obj, from_timezone, zone['timezone'])
            datetime_to_tz = datetime_tz_to_tz(datetime_to_obj, from_timezone, zone['timezone'])
            zone_id = zone['timezone'].replace('/','__')

            
            datetime_from_str = datetime_from_tz.strftime('%Y-%m-%d %H:%M')
            datetime_to_str = datetime_to_tz.strftime('%Y-%m-%d %H:%M')
            if format == 'split':
                datetime_from_str = datetime_from_tz.strftime('%Y-%m-%d')
                datetime_to_str = f'{datetime_from_tz.strftime("%H:%M")} - {datetime_to_tz.strftime("%H:%M")}'

            timezone_refs[zone_id].cells[0].content.disabled = False
            timezone_refs[zone_id].cells[1].content.value = datetime_from_str
            timezone_refs[zone_id].cells[1].content.opacity = 100
            timezone_refs[zone_id].cells[2].content.value = datetime_to_str
            timezone_refs[zone_id].cells[2].content.opacity = 100

        page.update()



    def timezones_display(datetime_obj=None, datetime_to_obj=None, datetime_string=None):

        disabled = True
        opacity = 0
        if datetime_string or datetime_obj:
            disabled = False
            opacity = 100

        if not datetime_string:
            datetime_string = date_now_string
        if datetime_obj:
            datetime_string = datetime_obj.strftime('%Y-%m-%d %H:%M')

        timezones = timezone_list()
        for zone in timezones:
            zone_id = zone['timezone'].replace('/','__')
            timezone_refs[zone_id] = ft.DataRow(
                cells=[
                    ft.DataCell(
                        ft.Switch(
                            label=zone['label'],
                            disabled=disabled,
                            on_change=timezone_enabled
                        )
                    ),
                    ft.DataCell(
                        ft.Text(
                            value=datetime_string,
                            opacity=opacity
                        )
                    ),
                    ft.DataCell(
                        ft.Text(
                            value=datetime_string,
                            opacity=opacity
                        )
                    )
                ]
            )

        timezone_rows = []
        for zone in timezones:
            zone_id = zone['timezone'].replace('/','__')
            timezone_rows.append(timezone_refs[zone_id])

        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Timezone")),
                ft.DataColumn(
                    ft.Text(
                        value=""
                    ),
                ),
                ft.DataColumn(
                    ft.Text(
                        value=""
                    ),
                )
            ],
            rows=timezone_rows,
            width=600
        )

    date_sel = date_selector()
    hour_sel_from = hour_selector()
    min_sel_from = minute_selector()
    hour_sel_to = hour_selector()
    min_sel_to = minute_selector()
    timezone_sel = timezone_selector()
    description_field = description_input()
    datetime_display = datetime_display_text()
    timezones_display_table = timezones_display()

    date_display_field = date_display()
    description_display_field = description_display()
    timezones_selected_display_table = timezones_selected_display([])

    background = background_image()


    page.on_resize = page_resize
    page.padding = 0

    # Route handler

    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    appbar(page),
                    ft.Stack(

                        [
                            background,
                            ft.Column(
                                [
                                    ft.Container(
                                        alignment=ft.alignment.center,
                                        content=description_display_field
                                    ),
                                    # ft.Container(
                                    #     alignment=ft.alignment.center,
                                    #     content=date_display_field
                                    # ),
                                    ft.Container(
                                        alignment=ft.alignment.center,
                                        content=timezones_selected_display_table
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                expand=1
                            )
                        ]
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                padding=0
            )
        )
        if page.route == "/settings":

            page.views.append(
                ft.View(
                    "/settings",
                    [
                        appbar(page),
                        ft.Row(
                            [
                                ft.Container(
                                    content=date_sel
                                ),
                                ft.Container(
                                    content=ft.Text("From:")
                                ),
                                ft.Container(
                                    content=hour_sel_from
                                ),
                                ft.Container(
                                    content=min_sel_from
                                ),
                                ft.Container(
                                    content=ft.Text("To:")
                                ),
                                ft.Container(
                                    content=hour_sel_to
                                ),
                                ft.Container(
                                    content=min_sel_to
                                ),
                                ft.Container(
                                    content=timezone_sel
                                )
                            ]
                        ),
                        ft.Container(
                            content=description_field
                        ),
                        ft.Container(
                            content=datetime_display
                        ),
                        ft.Container(
                            content=timezones_display_table
                        )
                    ],
                )
            )
        page.update()


    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


if __name__ == "__main__":

    ft.app(target=main, view=ft.WEB_BROWSER, port=8888)

