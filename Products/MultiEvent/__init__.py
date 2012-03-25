import os, os.path

from Globals import package_home

from Products.Archetypes import public
from Products.CMFCore import utils

from Products.MultiEvent import config

def initialize(context):
    import MultiEvent

    content_types, constructors, ftis = public.process_types(
        public.listTypes(config.PROJECTNAME),
        config.PROJECTNAME)

    utils.ContentInit(
        config.PROJECTNAME + ' Content',
        content_types      = content_types,
        permission         = config.ADD_CONTENT_PERMISSION,
        extra_constructors = constructors,
        fti                = ftis,
        ).initialize(context)

