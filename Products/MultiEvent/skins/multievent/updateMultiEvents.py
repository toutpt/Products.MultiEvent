## Script (Python) "updateMultiEvents"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
# to call with:  wget http://<user>:<passwd>@<host:port>/<portal>/updateMultiEvents

print DateTime()

catalog = container.portal_catalog
events = [b.getObject() for b in catalog(
                                    meta_type='MultiEvent',
                                    review_state='published'
                                   )]

member = context.portal_membership.getAuthenticatedMember()
if member.getId()!=None:
    for ev in events:
        print 'update event: %s'%ev.absolute_url()
        try:
            ev.updateEvent()
        except Exception, e:
            print '  error: %s.'%e
        else:
            print '  done.'

    print '# events:', len(events), 'all done.'
else:
    print 'Your user account does not have the required permission.'

return printed