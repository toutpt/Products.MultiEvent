MultiEvent README
=================

MultiEvent allows to manage similar events that take place in multiple dates and
locations using one content type.

Features
========

MultiEvent can be used to show all the standard informations of a Plone event,
plus some additional event dates and locations, in the future ("Next Events")
and/or in the past ("Past Events").

When the first event is expired and the MultiEvent is updated, the date and 
location of the first upcoming event appear in the main table and the old events
are archived as "Past Events".

MultiEvent shows all the standard informations of a Plone event, plus some
additional event dates and locations, in the future ("Next Events") and/or in
the past ("Past Events").

When the first event is expired, the date and location of the following will
appear in the main table.
Informations about the past events remain visible in the "Past Events" table .

Dependencies
============

DataGridField (version 1.5.0)


Usage and tips
==============

* Create a MultiEvent
* Add general event informations and a date
* Add additional dates and locations (optional)

Additional events must have a Location, a Start Date and an End Date.
Additional dates format is gg/mm/yy.

Events are rotated when the "updateEvent" method is called on the object URL; 
this can be done simply clicking the Update button.

When a MultiEvent is updated the main event data change accordingly.

It is possible to put the update URL in a Cron Job to automate the rotation.

Known issues
============

European date format are hardcoded
Integration with portlets is not provided yet
Validation on the sequence of the upcoming events is not provided for the End
Date

Credits
=======

MultiEvent written by Riccardo Lemmi - riccardo@reflab.com
packaged by JeanMichel FRANCOIS aka toutpt - toutpt@gmail.com

License
=======

Under GNU GPL


