
from copy import deepcopy

from DateTime import DateTime
from AccessControl import ClassSecurityInfo

from Products.Archetypes.public import *
from Products.CMFCore import permissions

from Products.ATContentTypes.content.event import ATEventSchema
from Products.ATContentTypes.content.event import ATEvent

from Products.MultiEvent.config import *
from Products.DataGridField import DataGridField, DataGridWidget
from Products.DataGridField.Column import Column

from Products.MultiEvent.utilities import *
from Products.MultiEvent import config

from i18n.messageid import MessageFactory
_ = MessageFactory('Products.MultiEvent')

schema = ATEventSchema.copy() + Schema((

    DataGridField('UpcomingEvents',
        columns=('location','startDate','endDate'),
        allow_reorder = False,
        widget = DataGridWidget(
            label=_(u'label_upcoming_events',
                    default=u'Upcoming Events'),
            description = _(u"help_upcoming_event",
                    default=u"Date must be in the day/month/Year format."),
            columns={'location' : Column(_(u"Location")),
                     'startDate' : Column(_(u"Start Date")),
                     'endDate' : Column(_(u"End Date")),
                    },),
        ),

    BooleanField('excludePastFromView',
        required = False,
        default = True,
        widget = BooleanWidget(
            label = _(u"label_exclude_past_from_view",
                      default=u"Exclude past events from view"),
            description=_(u"help_exclude_past_from_view",
                  default=u"If selected, past events will be not showed"),
            visible={'view' : 'hidden',
                     'edit' : 'visible'},
            ),
        ),

    DataGridField('PastEvents',
        columns=('location','startDate','endDate'),
        allow_reorder = False,
        allow_insert = False,
        widget = DataGridWidget(
            label=_(u"label_past_events", default='Past Events'),
            columns={'location' : Column(_(u"Location")),
                     'startDate' : Column(_(u"Start Date")),
                     'endDate' : Column(_(u"End Date")),
                    },),
        ),

))


class MultiEvent(ATEvent):
    """  """
    archetype_name = 'MultiEvent'
    portal_type    = 'MultiEvent'
    meta_type      = 'MultiEvent'

    global_allow               = 1
    allow_discussion           = 0
    default_view               = 'multi_event_view'
    immediate_view             = 'multi_event_view'
    schema                     = schema
    content_icon               = "event_icon.gif"
    security                   = ClassSecurityInfo()

    security.declareProtected(permissions.View, 'post_validate')
    def post_validate(self, REQUEST=None, errors={}):
        events = REQUEST.get('UpcomingEvents')
        if events:
            events = [event for event in events if not isEmptyEvent(event)]
            not_valid_events = [event for event in events if not isValidEvent(event)]
            if not_valid_events:
                errors['UpcomingEvents']="There is one or more not valid events"
                return

            upcoming_events = [event for event in events
                                if self.start().Date() > DateTimeFromFormattedString(event['startDate']).Date()]
            if upcoming_events:
                errors['UpcomingEvents']="There is one or more upcoming events before current event"
                return

    security.declarePrivate('at_post_create_script')
    def at_post_create_script(self):
        self.at_post_edit_script()

    security.declarePrivate('at_post_edit_script')
    def at_post_edit_script(self):
        # order upcoming events
        upcoming_events = self.getUpcomingEvents()
        sortable_events = [(event['startDate'], event) for event in upcoming_events]
        sortable_events.sort()
        ordered_events = [event[1] for event in sortable_events]
        self.setUpcomingEvents(ordered_events)

    def _addEvent(self, location, start, end):
        events = self.getUpcomingEvents()
        events += ( { 'location'  : location,
                      'startDate' : start,
                      'endDate'   : end,},)
        self.setUpcomingEvents(events)

    def _copyCurrentToPastEvents(self):
        past_events = self.getPastEvents()
        past_events = past_events + ({'startDate': date_in_formatted_string_format(self.start()),
                                      'endDate': date_in_formatted_string_format(self.end()),
                                      'location': self.getLocation()},)
        past_events = clear_from_invalid_events(past_events)
        self.setPastEvents(past_events)

    def _updateCurrentEvent(self, next_event):
          start_time = self.start().strftime('%H:%M')
          end_time = self.end().strftime('%H:%M')
          self.setStartDate(DateTimeFromFormattedString(next_event['startDate'], start_time))
          self.setEndDate(DateTimeFromFormattedString(next_event['startDate'], end_time))
          self.setLocation(next_event['location'])
          self.reindexObject()

    security.declareProtected(permissions.ModifyPortalContent, 'updateEvent')
    def updateEvent(self, REQUEST=None):
        """
            Update start, end date and location with the first row in Events
            Move current event in past events
            Events: must be ordered by startDate, see at_post_edit_script
        """
        events = clear_from_invalid_events(self.getUpcomingEvents())
        if events:
            next_event = events[0]
            next_event_startdate = DateTimeFromFormattedString(next_event['startDate'])
            today = DateTime()

            if self.start().Date() < today.Date() and today.Date() < next_event_startdate.Date():
                self._copyCurrentToPastEvents()
                self._updateCurrentEvent(next_event)
                # remove first event from UpcomingEvents
                remaining_events = events[1:]
                self.setUpcomingEvents(remaining_events)

        if REQUEST:
            REQUEST.RESPONSE.redirect(self.absolute_url())

    security.declareProtected(permissions.View, 'getUpcomingEventsAsDateTime')
    def getUpcomingEventsAsDateTime(self):
        """ """
        events = deepcopy(self.getRawUpcomingEvents())
        for e in events:
            e['startDate'] = DateTime(e['startDate'], datefmt='international')
            e['endDate'] = DateTime(e['endDate'], datefmt='international')

        return events

registerType(MultiEvent, config.PROJECTNAME)
