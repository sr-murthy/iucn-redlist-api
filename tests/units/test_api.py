# -- IMPORTS --

# -- Standard libraries --
import os
from unittest import mock
from urllib.parse import urlencode

# -- 3rd party libraries --
# -- Internal libraries --
from iucn_redlist_api.api import IucnRedListApiClient, IucnRedListApiSession
from iucn_redlist_api.constants import IUCN_RED_LIST_API_CONSTANTS as API_CONSTANTS


class _TestIucnRedListApi:
    _api_key = os.environ["API_KEY"]


class TestIucnRedListApiSession(_TestIucnRedListApi):
    def test_api_session(self):
        test_session = IucnRedListApiSession(self._api_key)

        assert test_session.api_key == self._api_key
        assert test_session.headers == {
            "Accept": "application/json",
            "Authorization": self._api_key,
        }


class TestIucnRedListApiClient(_TestIucnRedListApi):
    def test_api_client____init__(self):
        test_client = IucnRedListApiClient(self._api_key)

        assert test_client.api_session.api_key == self._api_key
        assert test_client.api_session.headers == {
            "Accept": "application/json",
            "Authorization": self._api_key,
        }
        assert test_client.api_version == API_CONSTANTS.API_VERSION.value

    def test_api_client__get(self):
        test_client = IucnRedListApiClient(self._api_key)
        BASEURL = API_CONSTANTS.BASEURL.value

        with mock.patch(
            "iucn_redlist_api.api.IucnRedListApiClient.api_session"
        ) as mock_client_session:
            # Assessments
            test_client.get("assessment/test_id")
            mock_client_session.get.assert_called_with(f"{BASEURL}/assessment/test_id")

            # Biogeographical realms
            test_client.get("biogeographical_realms")
            mock_client_session.get.assert_called_with(
                f"{BASEURL}/biogeographical_realms"
            )
            test_client.get("biogeographical_realms/test_code")
            mock_client_session.get.assert_called_with(
                f"{BASEURL}/biogeographical_realms/test_code"
            )

            # Comprehensive groups
            test_client.get("comprehensive_groups")
            mock_client_session.get.assert_called_with(
                f"{BASEURL}/comprehensive_groups"
            )
            test_client.get("comprehensive_groups/test_code")
            mock_client_session.get.assert_called_with(
                f"{BASEURL}/comprehensive_groups/test_code"
            )

            # Conservation actions
            test_client.get("conservation_actions")
            mock_client_session.get.assert_called_with(
                f"{BASEURL}/conservation_actions"
            )
            test_client.get("conservation_actions/test_code")
            mock_client_session.get.assert_called_with(
                f"{BASEURL}/conservation_actions/test_code"
            )

            # Countries
            test_client.get("countries")
            mock_client_session.get.assert_called_with(f"{BASEURL}/countries")
            test_client.get("countries/test_code")
            mock_client_session.get.assert_called_with(f"{BASEURL}/countries/test_code")

            # FAOs
            test_client.get("faos")
            mock_client_session.get.assert_called_with(f"{BASEURL}/faos")
            test_client.get("faos/test_code")
            mock_client_session.get.assert_called_with(f"{BASEURL}/faos/test_code")

            # Growth forms
            test_client.get("growth_forms")
            mock_client_session.get.assert_called_with(f"{BASEURL}/growth_forms")
            test_client.get("growth_forms/test_code")
            mock_client_session.get.assert_called_with(
                f"{BASEURL}/growth_forms/test_code"
            )

            # Green status
            test_client.get("green_status/all")
            mock_client_session.get.assert_called_with(f"{BASEURL}/green_status/all")

            # Habitat
            test_client.get("habitats")
            mock_client_session.get.assert_called_with(f"{BASEURL}/habitats")
            test_client.get("habitats/test_code")
            mock_client_session.get.assert_called_with(f"{BASEURL}/habitats/test_code")

            # Information
            test_client.get("information/api_version")
            mock_client_session.get.assert_called_with(
                f"{BASEURL}/information/api_version"
            )
            test_client.get("information/red_list_version")
            mock_client_session.get.assert_called_with(
                f"{BASEURL}/information/red_list_version"
            )

            # Population trends
            test_client.get("population_trends")
            mock_client_session.get.assert_called_with(f"{BASEURL}/population_trends")
            test_client.get("population_trends/test_code")
            mock_client_session.get.assert_called_with(
                f"{BASEURL}/population_trends/test_code"
            )

            # Red List categories
            test_client.get("red_list_categories")
            mock_client_session.get.assert_called_with(f"{BASEURL}/red_list_categories")
            test_client.get("red_list_categories/test_code")
            mock_client_session.get.assert_called_with(
                f"{BASEURL}/red_list_categories/test_code"
            )

            # Research
            test_client.get("research")
            mock_client_session.get.assert_called_with(f"{BASEURL}/research")
            test_client.get("research/test_code")
            mock_client_session.get.assert_called_with(f"{BASEURL}/research/test_code")

            # Scopes
            test_client.get("scopes")
            mock_client_session.get.assert_called_with(f"{BASEURL}/scopes")
            test_client.get("scopes/test_code")
            mock_client_session.get.assert_called_with(f"{BASEURL}/scopes/test_code")

            # Statistics
            test_client.get("statistics/count")
            mock_client_session.get.assert_called_with(f"{BASEURL}/statistics/count")

            # Stresses
            test_client.get("stresses")
            mock_client_session.get.assert_called_with(f"{BASEURL}/stresses")
            test_client.get("stresses/test_code")
            mock_client_session.get.assert_called_with(f"{BASEURL}/stresses/test_code")

            # Systems
            test_client.get("systems")
            mock_client_session.get.assert_called_with(f"{BASEURL}/systems")
            test_client.get("systems/test_code")
            mock_client_session.get.assert_called_with(f"{BASEURL}/systems/test_code")

            # Taxa - SIS by SIS code
            test_client.get("taxa/sis/test_sis_code")
            mock_client_session.get.assert_called_with(
                f"{BASEURL}/taxa/sis/test_sis_code"
            )

            # Taxa - Scientific name
            test_params = {
                "genus_name": "test_genus_name",
                "species_name": "test_species_name",
                "page": 1,
            }
            test_client.get("taxa/scientific_name", params=test_params)
            mock_client_session.get.assert_called_with(
                f"{BASEURL}/taxa/scientific_name?{urlencode(test_params)}"
            )

            # Taxa - Kingdom
            test_client.get("taxa/kingdom")
            mock_client_session.get.assert_called_with(f"{BASEURL}/taxa/kingdom")
            test_params = {"page": 1}
            test_client.get("taxa/kingdom/test_kingdom_name", params=test_params)
            mock_client_session.get.assert_called_with(
                f"{BASEURL}/taxa/kingdom/test_kingdom_name?{urlencode(test_params)}"
            )

            # Taxa - Phylum
            test_client.get("taxa/phylum")
            mock_client_session.get.assert_called_with(f"{BASEURL}/taxa/phylum")
            test_params = {"page": 1}
            test_client.get("taxa/phylum/test_phylum_name", params=test_params)
            mock_client_session.get.assert_called_with(
                f"{BASEURL}/taxa/phylum/test_phylum_name?{urlencode(test_params)}"
            )

            # Taxa - Phylum
            test_client.get("taxa/phylum")
            mock_client_session.get.assert_called_with(f"{BASEURL}/taxa/phylum")
            test_params = {"latest": True}
            test_client.get("taxa/phylum/test_phylum_name", params=test_params)
            mock_client_session.get.assert_called_with(
                f"{BASEURL}/taxa/phylum/test_phylum_name?{urlencode(test_params)}"
            )

            # Taxa - Class
            test_client.get("taxa/class")
            mock_client_session.get.assert_called_with(f"{BASEURL}/taxa/class")
            test_params = {"latest": True}
            test_client.get("taxa/class/test_class_name", params=test_params)
            mock_client_session.get.assert_called_with(
                f"{BASEURL}/taxa/class/test_class_name?{urlencode(test_params)}"
            )

            # Taxa - Order
            test_client.get("taxa/order")
            mock_client_session.get.assert_called_with(f"{BASEURL}/taxa/order")
            test_params = {"latest": True}
            test_client.get("taxa/order/test_order_name", params=test_params)
            mock_client_session.get.assert_called_with(
                f"{BASEURL}/taxa/order/test_order_name?{urlencode(test_params)}"
            )

            # Taxa - Family
            test_client.get("taxa/family")
            mock_client_session.get.assert_called_with(f"{BASEURL}/taxa/family")
            test_params = {"latest": True}
            test_client.get("taxa/family/test_family_name", params=test_params)
            mock_client_session.get.assert_called_with(
                f"{BASEURL}/taxa/family/test_family_name?{urlencode(test_params)}"
            )

            # Taxa - Extinction status
            test_client.get("taxa/possibly_extinct")
            mock_client_session.get.assert_called_with(
                f"{BASEURL}/taxa/possibly_extinct"
            )
            test_client.get("taxa/possibly_extinct_in_the_wild")
            mock_client_session.get.assert_called_with(
                f"{BASEURL}/taxa/possibly_extinct_in_the_wild"
            )

            # Threats
            test_client.get("threats")
            mock_client_session.get.assert_called_with(f"{BASEURL}/threats")
            test_client.get("threats/test_code")
            mock_client_session.get.assert_called_with(f"{BASEURL}/threats/test_code")

            # Use and trade
            test_client.get("use_and_trade")
            mock_client_session.get.assert_called_with(f"{BASEURL}/use_and_trade")
            test_client.get("use_and_trade/test_code")
            mock_client_session.get.assert_called_with(
                f"{BASEURL}/use_and_trade/test_code"
            )

    def test_get_assessment(self):
        test_client = IucnRedListApiClient(self._api_key)
        with mock.patch(
            "iucn_redlist_api.api.IucnRedListApiClient.get"
        ) as mock_client_get:
            test_client.get_assessment("test_assessment_id")
            mock_client_get.assert_called_with("assessment/test_assessment_id")

    def test_assessment_search(self):
        test_client = IucnRedListApiClient(self._api_key)
        with mock.patch(
            "iucn_redlist_api.api.IucnRedListApiClient.get"
        ) as mock_client_get:
            test_client.assessment_search(
                filter_on=["test_search_filter1", "test_search_filter2"], page=1
            )
            mock_client_get.assert_called_with(
                "assessment_search",
                params={
                    "filter_on[]": ["test_search_filter1", "test_search_filter2"],
                    "page": 1,
                },
            )

    def test_get_biogeographical_realms(self):
        test_client = IucnRedListApiClient(self._api_key)
        with mock.patch(
            "iucn_redlist_api.api.IucnRedListApiClient.get"
        ) as mock_client_get:
            test_client.get_biogeographical_realms()
            mock_client_get.assert_called_with("biogeographical_realms")

    def test_get_biogeographical_realm_assessments(self):
        test_client = IucnRedListApiClient(self._api_key)
        with mock.patch(
            "iucn_redlist_api.api.IucnRedListApiClient.get"
        ) as mock_client_get:
            test_client.get_biogeographical_realm_assessments("test_code", page=1)
            mock_client_get.assert_called_with(
                "biogeographical_realms/test_code", params={"page": 1}
            )

    def test_get_comprehensive_groups(self):
        test_client = IucnRedListApiClient(self._api_key)
        with mock.patch(
            "iucn_redlist_api.api.IucnRedListApiClient.get"
        ) as mock_client_get:
            test_client.get_comprehensive_groups()
            mock_client_get.assert_called_with("comprehensive_groups")

    def test_get_comprehensive_group_assessments(self):
        test_client = IucnRedListApiClient(self._api_key)
        with mock.patch(
            "iucn_redlist_api.api.IucnRedListApiClient.get"
        ) as mock_client_get:
            test_client.get_comprehensive_group_assessments("test_code", page=1)
            mock_client_get.assert_called_with(
                "comprehensive_groups/test_code", params={"page": 1}
            )

    def test_get_conservation_actions(self):
        test_client = IucnRedListApiClient(self._api_key)
        with mock.patch(
            "iucn_redlist_api.api.IucnRedListApiClient.get"
        ) as mock_client_get:
            test_client.get_conservation_actions()
            mock_client_get.assert_called_with("conservation_actions")

    def test_get_conservation_action_assessments(self):
        test_client = IucnRedListApiClient(self._api_key)
        with mock.patch(
            "iucn_redlist_api.api.IucnRedListApiClient.get"
        ) as mock_client_get:
            test_client.get_conservation_action_assessments("test_code", page=1)
            mock_client_get.assert_called_with(
                "conservation_actions/test_code", params={"page": 1}
            )

    def test_get_countries(self):
        test_client = IucnRedListApiClient(self._api_key)
        with mock.patch(
            "iucn_redlist_api.api.IucnRedListApiClient.get"
        ) as mock_client_get:
            test_client.get_countries()
            mock_client_get.assert_called_with("countries")

    def test_get_country_assessments(self):
        test_client = IucnRedListApiClient(self._api_key)
        with mock.patch(
            "iucn_redlist_api.api.IucnRedListApiClient.get"
        ) as mock_client_get:
            test_client.get_country_assessments("test_code", page=1)
            mock_client_get.assert_called_with(
                "countries/test_code", params={"page": 1}
            )

    def test_get_faos(self):
        test_client = IucnRedListApiClient(self._api_key)
        with mock.patch(
            "iucn_redlist_api.api.IucnRedListApiClient.get"
        ) as mock_client_get:
            test_client.get_faos()
            mock_client_get.assert_called_with("faos")

    def test_get_fao_assessments(self):
        test_client = IucnRedListApiClient(self._api_key)
        with mock.patch(
            "iucn_redlist_api.api.IucnRedListApiClient.get"
        ) as mock_client_get:
            test_client.get_fao_assessments("test_code", page=1)
            mock_client_get.assert_called_with("faos/test_code", params={"page": 1})

    def test_get_growth_forms(self):
        test_client = IucnRedListApiClient(self._api_key)
        with mock.patch(
            "iucn_redlist_api.api.IucnRedListApiClient.get"
        ) as mock_client_get:
            test_client.get_growth_forms()
            mock_client_get.assert_called_with("growth_forms")

    def test_get_growth_form_assessments(self):
        test_client = IucnRedListApiClient(self._api_key)
        with mock.patch(
            "iucn_redlist_api.api.IucnRedListApiClient.get"
        ) as mock_client_get:
            test_client.get_growth_form_assessments("test_code", page=1)
            mock_client_get.assert_called_with(
                "growth_forms/test_code", params={"page": 1}
            )

    def test_get_green_status_all(self):
        test_client = IucnRedListApiClient(self._api_key)
        with mock.patch(
            "iucn_redlist_api.api.IucnRedListApiClient.get"
        ) as mock_client_get:
            test_client.get_green_status_all()
            mock_client_get.assert_called_with("green_status/all")

    def test_get_habitats(self):
        test_client = IucnRedListApiClient(self._api_key)
        with mock.patch(
            "iucn_redlist_api.api.IucnRedListApiClient.get"
        ) as mock_client_get:
            test_client.get_habitats()
            mock_client_get.assert_called_with("habitats")

    def test_get_habitat_assessments(self):
        test_client = IucnRedListApiClient(self._api_key)
        with mock.patch(
            "iucn_redlist_api.api.IucnRedListApiClient.get"
        ) as mock_client_get:
            test_client.get_habitat_assessments("test_code", page=1)
            mock_client_get.assert_called_with("habitats/test_code", params={"page": 1})

    def test_get_information_api_version(self):
        test_client = IucnRedListApiClient(self._api_key)
        with mock.patch(
            "iucn_redlist_api.api.IucnRedListApiClient.get"
        ) as mock_client_get:
            test_client.get_information_api_version()
            mock_client_get.assert_called_with("information/api_version")

    def test_get_information_red_list_version(self):
        test_client = IucnRedListApiClient(self._api_key)
        with mock.patch(
            "iucn_redlist_api.api.IucnRedListApiClient.get"
        ) as mock_client_get:
            test_client.get_information_red_list_version()
            mock_client_get.assert_called_with("information/red_list_version")

    def test_get_population_trends(self):
        test_client = IucnRedListApiClient(self._api_key)
        with mock.patch(
            "iucn_redlist_api.api.IucnRedListApiClient.get"
        ) as mock_client_get:
            test_client.get_population_trends()
            mock_client_get.assert_called_with("population_trends")

    def test_get_population_trend_assessments(self):
        test_client = IucnRedListApiClient(self._api_key)
        with mock.patch(
            "iucn_redlist_api.api.IucnRedListApiClient.get"
        ) as mock_client_get:
            test_client.get_population_trend_assessments("test_code", page=1)
            mock_client_get.assert_called_with(
                "population_trends/test_code", params={"page": 1}
            )

    def test_get_red_list_categories(self):
        test_client = IucnRedListApiClient(self._api_key)
        with mock.patch(
            "iucn_redlist_api.api.IucnRedListApiClient.get"
        ) as mock_client_get:
            test_client.get_red_list_categories()
            mock_client_get.assert_called_with("red_list_categories")

    def test_get_red_list_category_assessments(self):
        test_client = IucnRedListApiClient(self._api_key)
        with mock.patch(
            "iucn_redlist_api.api.IucnRedListApiClient.get"
        ) as mock_client_get:
            test_client.get_red_list_category_assessments("test_code", page=1)
            mock_client_get.assert_called_with(
                "red_list_categories/test_code", params={"page": 1}
            )

    def test_get_research(self):
        test_client = IucnRedListApiClient(self._api_key)
        with mock.patch(
            "iucn_redlist_api.api.IucnRedListApiClient.get"
        ) as mock_client_get:
            test_client.get_research()
            mock_client_get.assert_called_with("research")

    def test_get_research_assessments(self):
        test_client = IucnRedListApiClient(self._api_key)
        with mock.patch(
            "iucn_redlist_api.api.IucnRedListApiClient.get"
        ) as mock_client_get:
            test_client.get_research_assessments("test_code", page=1)
            mock_client_get.assert_called_with("research/test_code", params={"page": 1})

    def test_get_scopes(self):
        test_client = IucnRedListApiClient(self._api_key)
        with mock.patch(
            "iucn_redlist_api.api.IucnRedListApiClient.get"
        ) as mock_client_get:
            test_client.get_scopes()
            mock_client_get.assert_called_with("scopes")

    def test_get_scope_assessments(self):
        test_client = IucnRedListApiClient(self._api_key)
        with mock.patch(
            "iucn_redlist_api.api.IucnRedListApiClient.get"
        ) as mock_client_get:
            test_client.get_scope_assessments("test_code", page=1)
            mock_client_get.assert_called_with("scopes/test_code", params={"page": 1})

    def test_get_statistics_count(self):
        test_client = IucnRedListApiClient(self._api_key)
        with mock.patch(
            "iucn_redlist_api.api.IucnRedListApiClient.get"
        ) as mock_client_get:
            test_client.get_statistics_count()
            mock_client_get.assert_called_with("statistics/count")

    def test_get_stresses(self):
        test_client = IucnRedListApiClient(self._api_key)
        with mock.patch(
            "iucn_redlist_api.api.IucnRedListApiClient.get"
        ) as mock_client_get:
            test_client.get_stresses()
            mock_client_get.assert_called_with("stresses")

    def test_get_stress_assessments(self):
        test_client = IucnRedListApiClient(self._api_key)
        with mock.patch(
            "iucn_redlist_api.api.IucnRedListApiClient.get"
        ) as mock_client_get:
            test_client.get_stress_assessments("test_code", page=1)
            mock_client_get.assert_called_with("stresses/test_code", params={"page": 1})

    def test_get_systems(self):
        test_client = IucnRedListApiClient(self._api_key)
        with mock.patch(
            "iucn_redlist_api.api.IucnRedListApiClient.get"
        ) as mock_client_get:
            test_client.get_systems()
            mock_client_get.assert_called_with("systems")

    def test_get_system_assessments(self):
        test_client = IucnRedListApiClient(self._api_key)
        with mock.patch(
            "iucn_redlist_api.api.IucnRedListApiClient.get"
        ) as mock_client_get:
            test_client.get_system_assessments("test_code", page=1)
            mock_client_get.assert_called_with("systems/test_code", params={"page": 1})

    def test_get_taxa_sis_assessments(self):
        test_client = IucnRedListApiClient(self._api_key)
        with mock.patch(
            "iucn_redlist_api.api.IucnRedListApiClient.get"
        ) as mock_client_get:
            test_client.get_taxa_sis_assessments("test_sis_id")
            mock_client_get.assert_called_with("taxa/sis/test_sis_id")

    def test_get_taxa_scientific_name_assessments(self):
        test_client = IucnRedListApiClient(self._api_key)
        with mock.patch(
            "iucn_redlist_api.api.IucnRedListApiClient.get"
        ) as mock_client_get:
            test_client.get_taxa_scientific_name_assessments(
                "test_genus_name", "test_species_name"
            )
            mock_client_get.assert_called_with(
                "taxa/scientific_name",
                params={
                    "genus_name": "test_genus_name",
                    "species_name": "test_species_name",
                },
            )

    def test_get_taxa_kingdom(self):
        test_client = IucnRedListApiClient(self._api_key)
        with mock.patch(
            "iucn_redlist_api.api.IucnRedListApiClient.get"
        ) as mock_client_get:
            test_client.get_taxa_kingdom()
            mock_client_get.assert_called_with("taxa/kingdom")

    def test_get_taxa_kingdom_assessments(self):
        test_client = IucnRedListApiClient(self._api_key)
        with mock.patch(
            "iucn_redlist_api.api.IucnRedListApiClient.get"
        ) as mock_client_get:
            test_client.get_taxa_kingdom_assessments("test_kingdom_name", page=1)
            mock_client_get.assert_called_with(
                "taxa/kingdom/test_kingdom_name", params={"page": 1}
            )

    def test_get_taxa_phylum(self):
        test_client = IucnRedListApiClient(self._api_key)
        with mock.patch(
            "iucn_redlist_api.api.IucnRedListApiClient.get"
        ) as mock_client_get:
            test_client.get_taxa_phylum()
            mock_client_get.assert_called_with("taxa/phylum")

    def test_get_taxa_phylum_assessments(self):
        test_client = IucnRedListApiClient(self._api_key)
        with mock.patch(
            "iucn_redlist_api.api.IucnRedListApiClient.get"
        ) as mock_client_get:
            test_client.get_taxa_phylum_assessments("test_phylum_name", latest=True)
            mock_client_get.assert_called_with(
                "taxa/phylum/test_phylum_name", params={"latest": True}
            )

    def test_get_taxa_class(self):
        test_client = IucnRedListApiClient(self._api_key)
        with mock.patch(
            "iucn_redlist_api.api.IucnRedListApiClient.get"
        ) as mock_client_get:
            test_client.get_taxa_class()
            mock_client_get.assert_called_with("taxa/class")

    def test_get_taxa_class_assessments(self):
        test_client = IucnRedListApiClient(self._api_key)
        with mock.patch(
            "iucn_redlist_api.api.IucnRedListApiClient.get"
        ) as mock_client_get:
            test_client.get_taxa_class_assessments("test_class_name", latest=True)
            mock_client_get.assert_called_with(
                "taxa/class/test_class_name", params={"latest": True}
            )

    def test_get_taxa_order(self):
        test_client = IucnRedListApiClient(self._api_key)
        with mock.patch(
            "iucn_redlist_api.api.IucnRedListApiClient.get"
        ) as mock_client_get:
            test_client.get_taxa_order()
            mock_client_get.assert_called_with("taxa/order")

    def test_get_taxa_order_assessments(self):
        test_client = IucnRedListApiClient(self._api_key)
        with mock.patch(
            "iucn_redlist_api.api.IucnRedListApiClient.get"
        ) as mock_client_get:
            test_client.get_taxa_order_assessments("test_order_name", latest=True)
            mock_client_get.assert_called_with(
                "taxa/order/test_order_name", params={"latest": True}
            )

    def test_get_taxa_family(self):
        test_client = IucnRedListApiClient(self._api_key)
        with mock.patch(
            "iucn_redlist_api.api.IucnRedListApiClient.get"
        ) as mock_client_get:
            test_client.get_taxa_family()
            mock_client_get.assert_called_with("taxa/family")

    def test_get_taxa_family_assessments(self):
        test_client = IucnRedListApiClient(self._api_key)
        with mock.patch(
            "iucn_redlist_api.api.IucnRedListApiClient.get"
        ) as mock_client_get:
            test_client.get_taxa_family_assessments("test_family_name", latest=True)
            mock_client_get.assert_called_with(
                "taxa/family/test_family_name", params={"latest": True}
            )

    def test_get_taxa_possibly_extinct(self):
        test_client = IucnRedListApiClient(self._api_key)
        with mock.patch(
            "iucn_redlist_api.api.IucnRedListApiClient.get"
        ) as mock_client_get:
            test_client.get_taxa_possibly_extinct()
            mock_client_get.assert_called_with("taxa/possibly_extinct")

    def test_get_taxa_possibly_extinct_in_the_wild(self):
        test_client = IucnRedListApiClient(self._api_key)
        with mock.patch(
            "iucn_redlist_api.api.IucnRedListApiClient.get"
        ) as mock_client_get:
            test_client.get_taxa_possibly_extinct_in_the_wild()
            mock_client_get.assert_called_with("taxa/possibly_extinct_in_the_wild")

    def test_get_threats(self):
        test_client = IucnRedListApiClient(self._api_key)
        with mock.patch(
            "iucn_redlist_api.api.IucnRedListApiClient.get"
        ) as mock_client_get:
            test_client.get_threats()
            mock_client_get.assert_called_with("threats")

    def test_get_threat_assessments(self):
        test_client = IucnRedListApiClient(self._api_key)
        with mock.patch(
            "iucn_redlist_api.api.IucnRedListApiClient.get"
        ) as mock_client_get:
            test_client.get_threat_assessments("test_code", page=1)
            mock_client_get.assert_called_with("threats/test_code", params={"page": 1})

    def test_get_use_and_trade(self):
        test_client = IucnRedListApiClient(self._api_key)
        with mock.patch(
            "iucn_redlist_api.api.IucnRedListApiClient.get"
        ) as mock_client_get:
            test_client.get_use_and_trade()
            mock_client_get.assert_called_with("use_and_trade")

    def test_get_use_and_trade_assessments(self):
        test_client = IucnRedListApiClient(self._api_key)
        with mock.patch(
            "iucn_redlist_api.api.IucnRedListApiClient.get"
        ) as mock_client_get:
            test_client.get_use_and_trade_assessments("test_code", page=1)
            mock_client_get.assert_called_with(
                "use_and_trade/test_code", params={"page": 1}
            )
