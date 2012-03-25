from plone.testing import z2

from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting, FunctionalTesting

class Layer(PloneSandboxLayer):
    default_bases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import Products.MultiEvent
        self.loadZCML(package=Products.MultiEvent)

        # Install product and call its initialize() function
        z2.installProduct(app, 'Products.MultiEvent')

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        self.applyProfile(portal, 'Products.MultiEvent:default')

    def tearDownZope(self, app):
        # Uninstall product
        z2.uninstallProduct(app, 'Products.MultiEvent')

FIXTURE = Layer()

INTEGRATION = IntegrationTesting(bases=(FIXTURE,),
                        name="Products.MultiEvent:Integration")
FUNCTIONAL = FunctionalTesting(bases=(FIXTURE,),
                        name="Products.MultiEvent:Functional")
