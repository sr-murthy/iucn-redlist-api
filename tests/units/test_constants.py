# -- IMPORTS --

# -- Standard libraries --

# -- 3rd party libraries --

# -- Internal libraries --
from iucn_redlist_api.constants import IUCN_RED_LIST_API_CONSTANTS as API_CONSTANTS


class TestIucnRedListApiConstants:
    def test_iucn_red_list_api_constants(self):
        assert API_CONSTANTS.DEVELOPER_PORTAL.value == "https://api.iucnredlist.org"
        assert API_CONSTANTS.API_VERSION.value == "v4"
        assert (
            API_CONSTANTS.API_REFERENCE.value
            == "https://api.iucnredlist.org/api-docs/index.html"
        )
        assert API_CONSTANTS.BASEURL.value == "https://api.iucnredlist.org/api/v4"
