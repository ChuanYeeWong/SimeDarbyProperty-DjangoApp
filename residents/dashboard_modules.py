from jet.dashboard.modules import DashboardModule
from residents.models import Resident,Request,Community,RequestFamily

class Total_Residents(DashboardModule):
    title = "Total Residents"
    template =  "dashboard/total_residents.html"
    
    def init_with_context(self, context):
        self.total = Resident.objects.all().count

class Pending_Request(DashboardModule):
    title = "Total Pending Resident Request"
    template = "dashboard/total_pending_request.html"

    def init_with_context(self,context):
        self.total = Request.objects.filter(status="P").count
class Pending_Family_Request(DashboardModule):
    title = "Total Pending Resident's Family Request"
    template = "dashboard/total_pending_family_request.html"

    def init_with_context(self,context):
        self.total = RequestFamily.objects.filter(status="P").count
class Display_Community (DashboardModule):
    title = "Community"
    template = "dashboard/display_community.html"

    def init_with_context(self,context):
        self.community = Community.objects.all()