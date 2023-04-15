from typing import List, Optional

from app.modules.organization.schema import Organization
from app.modules.subunit.schema import Subunit


class OrganizationSubunits(Organization):
    subunits: Optional[List[Subunit]] = None
