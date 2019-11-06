from django.utils.translation import ugettext_lazy as _
from jet.dashboard import modules
from jet.dashboard.dashboard import Dashboard, AppIndexDashboard
from residents import dashboard_modules

class CustomIndexDashboard(Dashboard):
    columns = 3

    def init_with_context(self, context):
        self.children.append(dashboard_modules.Total_Residents(_('Total Residents')))
        self.children.append(dashboard_modules.Pending_Request(_('Total Pending Resident Requests')))
        self.children.append(dashboard_modules.Pending_Family_Request(_('Total Pending Resident\'s Family Requests')))
        self.children.append(dashboard_modules.Display_Community(_('Community')))