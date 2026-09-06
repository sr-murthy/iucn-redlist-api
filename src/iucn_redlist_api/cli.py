# -- IMPORTS --

# -- Standard libraries --
import json
import os

# -- 3rd party libraries --
import click

# -- Internal libraries --
from iucn_redlist_api.api import IucnRedListApiClient


# ---------------------------------------------------------------------------#
# --- Global command group --------------------------------------------------#
# ---------------------------------------------------------------------------#
@click.group(
    "redlist-cli",
    help="IUCN Red List (of Threatened Species) API command line interface (CLI)",
)
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Global CLI debug mode - can be overridden in individual request-level commands",
)
@click.pass_context
def redlist_cli(ctx: click.Context, debug: bool):
    ctx.ensure_object(dict)

    ctx.obj["debug"] = debug
    ctx.obj["api_client"] = IucnRedListApiClient(
        os.environ["API_KEY"], debug_mode=debug
    )


@redlist_cli.command("api-version", help="Red List API version")
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Debug mode for the request and the response",
)
@click.pass_context
def api_version(ctx: click.Context, debug: bool):
    ctx.obj["api_client"].debug_mode = ctx.obj["debug"] or debug
    res_json = ctx.obj["api_client"].get_information_api_version().json
    click.echo(json.dumps(res_json, indent=4))


@redlist_cli.command("red-list-version", help="Red List version")
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Debug mode for the request and the response",
)
@click.pass_context
def version(ctx: click.Context, debug: bool):
    ctx.obj["api_client"].debug_mode = ctx.obj["debug"] or debug
    res_json = ctx.obj["api_client"].get_information_red_list_version().json
    click.echo(json.dumps(res_json, indent=4))


# ---------------------------------------------------------------------------#
# --- Assessment search command ---------------------------------------------#
# ---------------------------------------------------------------------------#


@redlist_cli.command(
    "assessment-search", help="Searches for assessment data based on search filters"
)
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Debug mode for the request and the response",
)
@click.option(
    "-f",
    "--filter-on",
    required=True,
    type=str,
    help="Comma-separated list of search criteria terms (str)",
)
@click.option(
    "-p",
    "--page-number",
    required=False,
    type=int,
    default=None,
    help="Optional page number in the response JSON, defaults to `None` (int)",
)
@click.pass_context
def assessment_search(
    ctx: click.Context, filter_on: str, page_number: int, debug: bool
) -> str:
    ctx.obj["api_client"].debug_mode = ctx.obj["debug"] or debug
    filter_on = list(map(str.strip, filter_on.split(",")))
    res_json = ctx.obj["api_client"].assessment_search(filter_on, page=page_number).json
    click.echo(json.dumps(res_json, indent=4))


# ---------------------------------------------------------------------------#
# --- Assessments command group ---------------------------------------------#
# ---------------------------------------------------------------------------#
@redlist_cli.group("assessments", help="Extinction risk assessments")
@click.pass_context
def assessments(ctx: click.Context): ...


@assessments.command("get", help="Assessment data for a specific assessment ID")
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Debug mode for the request and the response",
)
@click.option(
    "-a",
    "--assessment-id",
    required=True,
    type=int,
    help="Assessment ID (int)",
)
@click.pass_context
def get_assessment(ctx: click.Context, assessment_id: int, debug: bool) -> str:
    ctx.obj["api_client"].debug_mode = ctx.obj["debug"] or debug
    res_json = ctx.obj["api_client"].get_assessment(assessment_id).json
    click.echo(json.dumps(res_json, indent=4))


# ---------------------------------------------------------------------------#
# --- Biogeographical realms command group ----------------------------------#
# ---------------------------------------------------------------------------#
@redlist_cli.group("biogeographical-realms", help="Biogeographical realms")
@click.pass_context
def biogeographical_realms(ctx: click.Context): ...


@biogeographical_realms.command("get", help="Gets all biogeographical realms data")
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Debug mode for the request and the response",
)
@click.pass_context
def get_biogeographical_realms(ctx: click.Context, debug: bool) -> str:
    ctx.obj["api_client"].debug_mode = ctx.obj["debug"] or debug
    res_json = ctx.obj["api_client"].get_biogeographical_realms().json
    click.echo(json.dumps(res_json, indent=4))


@biogeographical_realms.command(
    "get-assessments",
    help="Assessment data related to a specific biogeographical realm by realm code",
)
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Debug mode for the request and the response",
)
@click.option(
    "-s",
    "--scope-code",
    required=False,
    type=int,
    default=None,
    help="Optional geographical assessment scope, defaults to `None` (int)",
)
@click.option(
    "--possibly-extinct-in-the-wild",
    is_flag=True,
    default=None,
    help="Optional indicator of species extinction in the wild status, defaults to `None`",
)
@click.option(
    "--possibly-extinct",
    is_flag=True,
    default=None,
    help="Optional indicator of species extinction status, defaults to `None`",
)
@click.option(
    "--latest",
    is_flag=True,
    default=None,
    help="Optional indicator of whether to get the latest assessments, defaults to `None`",
)
@click.option(
    "-y",
    "--year-published",
    required=False,
    type=str,
    default=None,
    help="Optional publication year number, defaults to `None` (int)",
)
@click.option(
    "-p",
    "--page-number",
    required=False,
    type=str,
    default=None,
    help="Optional page number in the response JSON, defaults to `None` (int)",
)
@click.option(
    "-r",
    "--realm-code",
    required=True,
    type=int,
    help="Biogeographical realm code (str)",
)
@click.pass_context
def get_biogeographical_realm_assessments(
    ctx: click.Context,
    realm_code: str,
    page_number: int,
    year_published: int,
    latest: bool,
    possibly_extinct: bool,
    possibly_extinct_in_the_wild: bool,
    scope_code: int,
    debug: bool,
) -> str:
    ctx.obj["api_client"].debug_mode = ctx.obj["debug"] or debug
    res_json = (
        ctx.obj["api_client"]
        .get_biogeographical_realm_assessments(
            realm_code,
            page=page_number,
            year_published=year_published,
            latest=latest,
            possibly_extinct=possibly_extinct,
            possibly_extinct_in_the_wild=possibly_extinct_in_the_wild,
            scope_code=scope_code,
        )
        .json
    )
    click.echo(json.dumps(res_json, indent=4))


# ---------------------------------------------------------------------------#
# --- Comprehensive groups command group ------------------------------------#
# ---------------------------------------------------------------------------#
@redlist_cli.group("comprehensive-groups", help="Comprehensive groups")
@click.pass_context
def comprehensive_groups(ctx: click.Context): ...


@comprehensive_groups.command("get", help="Gets all comprehensive groups data")
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Debug mode for the request and the response",
)
@click.pass_context
def get_comprehensive_groups(ctx: click.Context, debug: bool) -> str:
    ctx.obj["api_client"].debug_mode = ctx.obj["debug"] or debug
    res_json = ctx.obj["api_client"].get_comprehensive_groups().json
    click.echo(json.dumps(res_json, indent=4))


@comprehensive_groups.command(
    "get-assessments",
    help="Assessment data related to a specific comprehensive group by group name",
)
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Debug mode for the request and the response",
)
@click.option(
    "-s",
    "--scope-code",
    required=False,
    type=int,
    default=None,
    help="Optional geographical assessment scope, defaults to `None` (int)",
)
@click.option(
    "--possibly-extinct-in-the-wild",
    is_flag=True,
    default=None,
    help="Optional indicator of species extinction in the wild status, defaults to `None`",
)
@click.option(
    "--possibly-extinct",
    is_flag=True,
    default=None,
    help="Optional indicator of species extinction status, defaults to `None`",
)
@click.option(
    "--latest",
    is_flag=True,
    default=None,
    help="Optional indicator of whether to get the latest assessments, defaults to `None`",
)
@click.option(
    "-y",
    "--year-published",
    required=False,
    type=str,
    default=None,
    help="Optional publication year number, defaults to `None` (int)",
)
@click.option(
    "-p",
    "--page-number",
    required=False,
    type=str,
    default=None,
    help="Optional page number in the response JSON, defaults to `None` (int)",
)
@click.option(
    "-g", "--group-name", required=True, type=str, help="Comprehensive group name (str)"
)
@click.pass_context
def get_comprehensive_group_assessments(
    ctx: click.Context,
    group_name: str,
    page_number: int,
    year_published: int,
    latest: bool,
    possibly_extinct: bool,
    possibly_extinct_in_the_wild: bool,
    scope_code: int,
    debug: bool,
) -> str:
    ctx.obj["api_client"].debug_mode = ctx.obj["debug"] or debug
    res_json = (
        ctx.obj["api_client"]
        .get_comprehensive_group_assessments(
            group_name,
            page=page_number,
            year_published=year_published,
            latest=latest,
            possibly_extinct=possibly_extinct,
            possibly_extinct_in_the_wild=possibly_extinct_in_the_wild,
            scope_code=scope_code,
        )
        .json
    )
    click.echo(json.dumps(res_json, indent=4))


# ---------------------------------------------------------------------------#
# --- Conservation actions command group ------------------------------------#
# ---------------------------------------------------------------------------#
@redlist_cli.group("conservation-actions", help="Conservation actions")
@click.pass_context
def conservation_actions(ctx: click.Context): ...


@conservation_actions.command("get", help="Gets all conservation_actions data")
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Debug mode for the request and the response",
)
@click.pass_context
def get_cooservation_actions(ctx: click.Context, debug: bool) -> str:
    ctx.obj["api_client"].debug_mode = ctx.obj["debug"] or debug
    res_json = ctx.obj["api_client"].get_conservation_actions().json
    click.echo(json.dumps(res_json, indent=4))


@conservation_actions.command(
    "get-assessments",
    help="Assessment data related to a specific conservation_action by action code",
)
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Debug mode for the request and the response",
)
@click.option(
    "-s",
    "--scope-code",
    required=False,
    type=int,
    default=None,
    help="Optional geographical assessment scope, defaults to `None` (int)",
)
@click.option(
    "--possibly-extinct-in-the-wild",
    is_flag=True,
    default=None,
    help="Optional indicator of species extinction in the wild status, defaults to `None`",
)
@click.option(
    "--possibly-extinct",
    is_flag=True,
    default=None,
    help="Optional indicator of species extinction status, defaults to `None`",
)
@click.option(
    "--latest",
    is_flag=True,
    default=None,
    help="Optional indicator of whether to get the latest assessments, defaults to `None`",
)
@click.option(
    "-y",
    "--year-published",
    required=False,
    type=str,
    default=None,
    help="Optional publication year number, defaults to `None` (int)",
)
@click.option(
    "-p",
    "--page-number",
    required=False,
    type=str,
    default=None,
    help="Optional page number in the response JSON, defaults to `None` (int)",
)
@click.option(
    "-a",
    "--action-code",
    required=True,
    type=str,
    help="Conservation action code (str)",
)
@click.pass_context
def get_conservation_action_assessments(
    ctx: click.Context,
    action_code: str,
    page_number: int,
    year_published: int,
    latest: bool,
    possibly_extinct: bool,
    possibly_extinct_in_the_wild: bool,
    scope_code: int,
    debug: bool,
) -> str:
    ctx.obj["api_client"].debug_mode = ctx.obj["debug"] or debug
    res_json = (
        ctx.obj["api_client"]
        .get_conservation_action_assessments(
            action_code,
            page=page_number,
            year_published=year_published,
            latest=latest,
            possibly_extinct=possibly_extinct,
            possibly_extinct_in_the_wild=possibly_extinct_in_the_wild,
            scope_code=scope_code,
        )
        .json
    )
    click.echo(json.dumps(res_json, indent=4))


# ---------------------------------------------------------------------------#
# --- Countries command group -----------------------------------------------#
# ---------------------------------------------------------------------------#
@redlist_cli.group(
    "countries",
    help="Countries (country names and ISO alpha-2 codes)",
)
@click.pass_context
def countries(ctx: click.Context): ...


@countries.command("get", help="Gets all countries data")
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Debug mode for the request and the response",
)
@click.pass_context
def get_countries(ctx: click.Context, debug: bool) -> str:
    ctx.obj["api_client"].debug_mode = ctx.obj["debug"] or debug
    res_json = ctx.obj["api_client"].get_countries().json
    click.echo(json.dumps(res_json, indent=4))


@countries.command(
    "get-assessments",
    help="Assessment data related to a specific country by ISO alpha-2 code",
)
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Debug mode for the request and the response",
)
@click.option(
    "-s",
    "--scope-code",
    required=False,
    type=int,
    default=None,
    help="Optional geographical assessment scope, defaults to `None` (int)",
)
@click.option(
    "--possibly-extinct-in-the-wild",
    is_flag=True,
    default=None,
    help="Optional indicator of species extinction in the wild status, defaults to `None`",
)
@click.option(
    "--possibly-extinct",
    is_flag=True,
    default=None,
    help="Optional indicator of species extinction status, defaults to `None`",
)
@click.option(
    "--latest",
    is_flag=True,
    default=None,
    help="Optional indicator of whether to get the latest assessments, defaults to `None`",
)
@click.option(
    "-y",
    "--year-published",
    required=False,
    type=str,
    default=None,
    help="Optional publication year number, defaults to `None` (int)",
)
@click.option(
    "-p",
    "--page-number",
    required=False,
    type=str,
    default=None,
    help="Optional page number in the response JSON, defaults to `None` (int)",
)
@click.option(
    "-c",
    "--country-code",
    required=True,
    type=str,
    help="Country ISO alpha-2 code (str)",
)
@click.pass_context
def get_country_assessments(
    ctx: click.Context,
    country_code: str,
    page_number: int,
    year_published: int,
    latest: bool,
    possibly_extinct: bool,
    possibly_extinct_in_the_wild: bool,
    scope_code: int,
    debug: bool,
) -> str:
    ctx.obj["api_client"].debug_mode = ctx.obj["debug"] or debug
    res_json = (
        ctx.obj["api_client"]
        .get_country_assessments(
            country_code,
            page=page_number,
            year_published=year_published,
            latest=latest,
            possibly_extinct=possibly_extinct,
            possibly_extinct_in_the_wild=possibly_extinct_in_the_wild,
            scope_code=scope_code,
        )
        .json
    )
    click.echo(json.dumps(res_json, indent=4))


# ---------------------------------------------------------------------------#
# --- Food & Agriculture Organization (FAO) fishing areas command group -----#
# ---------------------------------------------------------------------------#
@redlist_cli.group(
    "faos",
    help="Food and Agriculture Organization (FAO) international fishing areas data, including FAO fishing area codes",
)
@click.pass_context
def faos(ctx: click.Context): ...


@faos.command("get", help="FAO fishing areas data")
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Debug mode for the request and the response",
)
@click.pass_context
def get_faos(ctx: click.Context, debug: bool) -> str:
    ctx.obj["api_client"].debug_mode = ctx.obj["debug"] or debug
    res_json = ctx.obj["api_client"].get_faos().json
    click.echo(json.dumps(res_json, indent=4))


@faos.command(
    "get-assessments",
    help="Assessment data related to a specific FAO international fishing area by FAO code",
)
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Debug mode for the request and the response",
)
@click.option(
    "-s",
    "--scope-code",
    required=False,
    type=int,
    default=None,
    help="Optional geographical assessment scope, defaults to `None` (int)",
)
@click.option(
    "--possibly-extinct-in-the-wild",
    is_flag=True,
    default=None,
    help="Optional indicator of species extinction in the wild status, defaults to `None`",
)
@click.option(
    "--possibly-extinct",
    is_flag=True,
    default=None,
    help="Optional indicator of species extinction status, defaults to `None`",
)
@click.option(
    "--latest",
    is_flag=True,
    default=None,
    help="Optional indicator of whether to get the latest assessments, defaults to `None`",
)
@click.option(
    "-y",
    "--year-published",
    required=False,
    type=str,
    default=None,
    help="Optional publication year number, defaults to `None` (int)",
)
@click.option(
    "-p",
    "--page-number",
    required=False,
    type=str,
    default=None,
    help="Optional page number in the response JSON, defaults to `None` (int)",
)
@click.option(
    "-f",
    "--fao-code",
    required=True,
    type=str,
    help="FAO international fishing areas code (str)",
)
@click.pass_context
def get_fao_assessments(
    ctx: click.Context,
    fao_code: str,
    page_number: int,
    year_published: int,
    latest: bool,
    possibly_extinct: bool,
    possibly_extinct_in_the_wild: bool,
    scope_code: int,
    debug: bool,
) -> str:
    ctx.obj["api_client"].debug_mode = ctx.obj["debug"] or debug
    res_json = (
        ctx.obj["api_client"]
        .get_fao_assessments(
            fao_code,
            page=page_number,
            year_published=year_published,
            latest=latest,
            possibly_extinct=possibly_extinct,
            possibly_extinct_in_the_wild=possibly_extinct_in_the_wild,
            scope_code=scope_code,
        )
        .json
    )
    click.echo(json.dumps(res_json, indent=4))


# ---------------------------------------------------------------------------#
# --- Growth forms command group --------------------------------------------#
# ---------------------------------------------------------------------------#
@redlist_cli.group("growth-forms", help="Growth forms")
@click.pass_context
def growth_forms(ctx: click.Context): ...


@growth_forms.command("get", help="Growth forms data")
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Debug mode for the request and the response",
)
@click.pass_context
def get_growth_forms(ctx: click.Context, debug: bool) -> str:
    ctx.obj["api_client"].debug_mode = ctx.obj["debug"] or debug
    res_json = ctx.obj["api_client"].get_growth_forms().json
    click.echo(json.dumps(res_json, indent=4))


@growth_forms.command(
    "get-assessments",
    help="Assessment data related to a specific growth form by growth form code",
)
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Debug mode for the request and the response",
)
@click.option(
    "-s",
    "--scope-code",
    required=False,
    type=int,
    default=None,
    help="Optional geographical assessment scope, defaults to `None` (int)",
)
@click.option(
    "--possibly-extinct-in-the-wild",
    is_flag=True,
    default=None,
    help="Optional indicator of species extinction in the wild status, defaults to `None`",
)
@click.option(
    "--possibly-extinct",
    is_flag=True,
    default=None,
    help="Optional indicator of species extinction status, defaults to `None`",
)
@click.option(
    "--latest",
    is_flag=True,
    default=None,
    help="Optional indicator of whether to get the latest assessments, defaults to `None`",
)
@click.option(
    "-y",
    "--year-published",
    required=False,
    type=str,
    default=None,
    help="Optional publication year number, defaults to `None` (int)",
)
@click.option(
    "-p",
    "--page-number",
    required=False,
    type=str,
    default=None,
    help="Optional page number in the response JSON, defaults to `None` (int)",
)
@click.option(
    "-g", "--growth-form-code", required=True, type=str, help="Growth form code (str)"
)
@click.pass_context
def get_growth_form_assessments(
    ctx: click.Context,
    growth_form_code: str,
    page_number: int,
    year_published: int,
    latest: bool,
    possibly_extinct: bool,
    possibly_extinct_in_the_wild: bool,
    scope_code: int,
    debug: bool,
) -> str:
    ctx.obj["api_client"].debug_mode = ctx.obj["debug"] or debug
    res_json = (
        ctx.obj["api_client"]
        .get_growth_form_assessments(
            growth_form_code,
            page=page_number,
            year_published=year_published,
            latest=latest,
            possibly_extinct=possibly_extinct,
            possibly_extinct_in_the_wild=possibly_extinct_in_the_wild,
            scope_code=scope_code,
        )
        .json
    )
    click.echo(json.dumps(res_json, indent=4))


# ---------------------------------------------------------------------------#
# --- Green status command group --------------------------------------------#
# ---------------------------------------------------------------------------#
@redlist_cli.group(
    "green-status", help="Species green status (status of recovery and conservation)"
)
@click.pass_context
def green_status(ctx: click.Context): ...


@green_status.command("get-all", help="All green status assessments data")
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Debug mode for the request and the response",
)
@click.pass_context
def get_green_status_all(ctx: click.Context, debug: bool) -> str:
    ctx.obj["api_client"].debug_mode = ctx.obj["debug"] or debug
    res_json = ctx.obj["api_client"].get_green_status_all().json
    click.echo(json.dumps(res_json, indent=4))


# ---------------------------------------------------------------------------#
# --- Habitats command group ------------------------------------------------#
# ---------------------------------------------------------------------------#
@redlist_cli.group("habitats", help="Habitats")
@click.pass_context
def habitats(ctx: click.Context): ...


@habitats.command("get", help="Gets all habitats data")
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Debug mode for the request and the response",
)
@click.pass_context
def get_habitats(ctx: click.Context, debug: bool) -> str:
    ctx.obj["api_client"].debug_mode = ctx.obj["debug"] or debug
    res_json = ctx.obj["api_client"].get_habitats().json
    click.echo(json.dumps(res_json, indent=4))


@habitats.command(
    "get-assessments",
    help="Assessment data related to a specific habitat by habitat code",
)
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Debug mode for the request and the response",
)
@click.option(
    "-s",
    "--scope-code",
    required=False,
    type=int,
    default=None,
    help="Optional geographical assessment scope, defaults to `None` (int)",
)
@click.option(
    "--possibly-extinct-in-the-wild",
    is_flag=True,
    default=None,
    help="Optional indicator of species extinction in the wild status, defaults to `None`",
)
@click.option(
    "--possibly-extinct",
    is_flag=True,
    default=None,
    help="Optional indicator of species extinction status, defaults to `None`",
)
@click.option(
    "--latest",
    is_flag=True,
    default=None,
    help="Optional indicator of whether to get the latest assessments, defaults to `None`",
)
@click.option(
    "-y",
    "--year-published",
    required=False,
    type=str,
    default=None,
    help="Optional publication year number, defaults to `None` (int)",
)
@click.option(
    "-p",
    "--page-number",
    required=False,
    type=str,
    default=None,
    help="Optional page number in the response JSON, defaults to `None` (int)",
)
@click.option(
    "-h", "--habitat-code", required=True, type=str, help="Habitat code (str)"
)
@click.pass_context
def get_habitat_assessments(
    ctx: click.Context,
    habitat_code: str,
    page_number: int,
    year_published: int,
    latest: bool,
    possibly_extinct: bool,
    possibly_extinct_in_the_wild: bool,
    scope_code: int,
    debug: bool,
) -> str:
    ctx.obj["api_client"].debug_mode = ctx.obj["debug"] or debug
    res_json = (
        ctx.obj["api_client"]
        .get_habitat_assessments(
            habitat_code,
            page=page_number,
            year_published=year_published,
            latest=latest,
            possibly_extinct=possibly_extinct,
            possibly_extinct_in_the_wild=possibly_extinct_in_the_wild,
            scope_code=scope_code,
        )
        .json
    )
    click.echo(json.dumps(res_json, indent=4))


# ---------------------------------------------------------------------------#
# --- Information command group ---------------------------------------------#
# ---------------------------------------------------------------------------#
@redlist_cli.group("information", help="Red List and Red List API information")
@click.pass_context
def information(ctx: click.Context): ...


@information.command("red-list-api-version", help="Red List API version")
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Debug mode for the request and the response",
)
@click.pass_context
def info_api_version(ctx: click.Context, debug: bool):
    ctx.obj["api_client"].debug_mode = ctx.obj["debug"] or debug
    res_json = ctx.obj["api_client"].get_information_api_version().json
    click.echo(json.dumps(res_json, indent=4))


@information.command("red-list-version", help="Red List version")
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Debug mode for the request and the response",
)
@click.pass_context
def info_version(ctx: click.Context, debug: bool):
    ctx.obj["api_client"].debug_mode = ctx.obj["debug"] or debug
    res_json = ctx.obj["api_client"].get_information_red_list_version().json
    click.echo(json.dumps(res_json, indent=4))


# ---------------------------------------------------------------------------#
# --- Population trends command group ---------------------------------------#
# ---------------------------------------------------------------------------#
@redlist_cli.group("population-trends", help="Population trends")
@click.pass_context
def population_trends(ctx: click.Context): ...


@population_trends.command("get", help="Gets all population trends data")
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Debug mode for the request and the response",
)
@click.pass_context
def get_population_trends(ctx: click.Context, debug: bool) -> str:
    ctx.obj["api_client"].debug_mode = ctx.obj["debug"] or debug
    res_json = ctx.obj["api_client"].get_population_trends().json
    click.echo(json.dumps(res_json, indent=4))


@population_trends.command(
    "get-assessments",
    help="Assessment data related to a specific population trend by trend code",
)
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Debug mode for the request and the response",
)
@click.option(
    "-s",
    "--scope-code",
    required=False,
    type=int,
    default=None,
    help="Optional geographical assessment scope, defaults to `None` (int)",
)
@click.option(
    "--possibly-extinct-in-the-wild",
    is_flag=True,
    default=None,
    help="Optional indicator of species extinction in the wild status, defaults to `None`",
)
@click.option(
    "--possibly-extinct",
    is_flag=True,
    default=None,
    help="Optional indicator of species extinction status, defaults to `None`",
)
@click.option(
    "--latest",
    is_flag=True,
    default=None,
    help="Optional indicator of whether to get the latest assessments, defaults to `None`",
)
@click.option(
    "-y",
    "--year-published",
    required=False,
    type=str,
    default=None,
    help="Optional publication year number, defaults to `None` (int)",
)
@click.option(
    "-p",
    "--page-number",
    required=False,
    type=str,
    default=None,
    help="Optional page number in the response JSON, defaults to `None` (int)",
)
@click.option(
    "-t", "--trend-code", required=True, type=str, help="Population trend code (str)"
)
@click.pass_context
def get_population_trend_assessments(
    ctx: click.Context,
    trend_code: str,
    page_number: int,
    year_published: int,
    latest: bool,
    possibly_extinct: bool,
    possibly_extinct_in_the_wild: bool,
    scope_code: int,
    debug: bool,
) -> str:
    ctx.obj["api_client"].debug_mode = ctx.obj["debug"] or debug
    res_json = (
        ctx.obj["api_client"]
        .get_population_trend_assessments(
            trend_code,
            page=page_number,
            year_published=year_published,
            latest=latest,
            possibly_extinct=possibly_extinct,
            possibly_extinct_in_the_wild=possibly_extinct_in_the_wild,
            scope_code=scope_code,
        )
        .json
    )
    click.echo(json.dumps(res_json, indent=4))


# ---------------------------------------------------------------------------#
# --- Red List categories command group -------------------------------------#
# ---------------------------------------------------------------------------#
@redlist_cli.group(
    "red-list-categories",
    help="Red List extinction risk categories",
)
@click.pass_context
def red_list_categories(ctx: click.Context): ...


@red_list_categories.command("get", help="Red List categories data")
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Debug mode for the request and the response",
)
@click.pass_context
def get_red_list_categories(ctx: click.Context, debug: bool) -> str:
    ctx.obj["api_client"].debug_mode = ctx.obj["debug"] or debug
    res_json = ctx.obj["api_client"].get_red_list_categories().json
    click.echo(json.dumps(res_json, indent=4))


@red_list_categories.command(
    "get-assessments",
    help="Assessment data related to a specific Red List category by category code",
)
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Debug mode for the request and the response",
)
@click.option(
    "-s",
    "--scope-code",
    required=False,
    type=int,
    default=None,
    help="Optional geographical assessment scope, defaults to `None` (int)",
)
@click.option(
    "--possibly-extinct-in-the-wild",
    is_flag=True,
    default=None,
    help="Optional indicator of species extinction in the wild status, defaults to `None`",
)
@click.option(
    "--possibly-extinct",
    is_flag=True,
    default=None,
    help="Optional indicator of species extinction status, defaults to `None`",
)
@click.option(
    "--latest",
    is_flag=True,
    default=None,
    help="Optional indicator of whether to get the latest assessments, defaults to `None`",
)
@click.option(
    "-y",
    "--year-published",
    required=False,
    type=str,
    default=None,
    help="Optional publication year number, defaults to `None` (int)",
)
@click.option(
    "-p",
    "--page-number",
    required=False,
    type=str,
    default=None,
    help="Optional page number in the response JSON, defaults to `None` (int)",
)
@click.option(
    "-c",
    "--category-code",
    required=True,
    type=str,
    help="Red List category code (str)",
)
@click.pass_context
def get_red_list_category_assessments(
    ctx: click.Context,
    category_code: str,
    page_number: int,
    year_published: int,
    latest: bool,
    possibly_extinct: bool,
    possibly_extinct_in_the_wild: bool,
    scope_code: int,
    debug: bool,
) -> str:
    ctx.obj["api_client"].debug_mode = ctx.obj["debug"] or debug
    res_json = (
        ctx.obj["api_client"]
        .get_red_list_category_assessments(
            category_code,
            page=page_number,
            year_published=year_published,
            latest=latest,
            possibly_extinct=possibly_extinct,
            possibly_extinct_in_the_wild=possibly_extinct_in_the_wild,
            scope_code=scope_code,
        )
        .json
    )
    click.echo(json.dumps(res_json, indent=4))


# ---------------------------------------------------------------------------#
# --- Research categories command group -------------------------------------#
# ---------------------------------------------------------------------------#
@redlist_cli.group("research", help="Research categories")
@click.pass_context
def research(ctx: click.Context): ...


@research.command("get", help="Research categories data")
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Debug mode for the request and the response",
)
@click.pass_context
def get_research(ctx: click.Context, debug: bool) -> str:
    ctx.obj["api_client"].debug_mode = ctx.obj["debug"] or debug
    res_json = ctx.obj["api_client"].get_research().json
    click.echo(json.dumps(res_json, indent=4))


@research.command(
    "get-assessments",
    help="Assessment data related to a specific research category by research category code",
)
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Debug mode for the request and the response",
)
@click.option(
    "-s",
    "--scope-code",
    required=False,
    type=int,
    default=None,
    help="Optional geographical assessment scope, defaults to `None` (int)",
)
@click.option(
    "--possibly-extinct-in-the-wild",
    is_flag=True,
    default=None,
    help="Optional indicator of species extinction in the wild status, defaults to `None`",
)
@click.option(
    "--possibly-extinct",
    is_flag=True,
    default=None,
    help="Optional indicator of species extinction status, defaults to `None`",
)
@click.option(
    "--latest",
    is_flag=True,
    default=None,
    help="Optional indicator of whether to get the latest assessments, defaults to `None`",
)
@click.option(
    "-y",
    "--year-published",
    required=False,
    type=str,
    default=None,
    help="Optional publication year number, defaults to `None` (int)",
)
@click.option(
    "-p",
    "--page-number",
    required=False,
    type=str,
    default=None,
    help="Optional page number in the response JSON, defaults to `None` (int)",
)
@click.option(
    "-r",
    "--research-code",
    required=True,
    type=str,
    help="Research category code (str)",
)
@click.pass_context
def get_research_assessments(
    ctx: click.Context,
    research_code: str,
    page_number: int,
    year_published: int,
    latest: bool,
    possibly_extinct: bool,
    possibly_extinct_in_the_wild: bool,
    scope_code: int,
    debug: bool,
) -> str:
    ctx.obj["api_client"].debug_mode = ctx.obj["debug"] or debug
    res_json = (
        ctx.obj["api_client"]
        .get_research_assessments(
            research_code,
            page=page_number,
            year_published=year_published,
            latest=latest,
            possibly_extinct=possibly_extinct,
            possibly_extinct_in_the_wild=possibly_extinct_in_the_wild,
            scope_code=scope_code,
        )
        .json
    )
    click.echo(json.dumps(res_json, indent=4))


# ---------------------------------------------------------------------------#
# --- Geographic assessment scopes command group ----------------------------#
# ---------------------------------------------------------------------------#
@redlist_cli.group("scopes", help="Geographic assessment scopes")
@click.pass_context
def scopes(ctx: click.Context): ...


@scopes.command("get", help="Geographic assessment scopes data")
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Debug mode for the request and the response",
)
@click.pass_context
def get_scopes(ctx: click.Context, debug: bool) -> str:
    ctx.obj["api_client"].debug_mode = ctx.obj["debug"] or debug
    res_json = ctx.obj["api_client"].get_scopes().json
    click.echo(json.dumps(res_json, indent=4))


@scopes.command(
    "get-assessments",
    help="Assessment data related to a specific geographic assessment scope by scope code",
)
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Debug mode for the request and the response",
)
@click.option(
    "--possibly-extinct-in-the-wild",
    is_flag=True,
    default=None,
    help="Optional indicator of species extinction in the wild status, defaults to `None`",
)
@click.option(
    "--possibly-extinct",
    is_flag=True,
    default=None,
    help="Optional indicator of species extinction status, defaults to `None`",
)
@click.option(
    "--latest",
    is_flag=True,
    default=None,
    help="Optional indicator of whether to get the latest assessments, defaults to `None`",
)
@click.option(
    "-y",
    "--year-published",
    required=False,
    type=str,
    default=None,
    help="Optional publication year number, defaults to `None` (int)",
)
@click.option(
    "-p",
    "--page-number",
    required=False,
    type=str,
    default=None,
    help="Optional page number in the response JSON, defaults to `None` (int)",
)
@click.option(
    "-s",
    "--scope-code",
    required=True,
    type=str,
    help="Geographic assessment scope code (str)",
)
@click.pass_context
def get_scope_assessments(
    ctx: click.Context,
    page_number: int,
    year_published: int,
    latest: bool,
    possibly_extinct: bool,
    possibly_extinct_in_the_wild: bool,
    scope_code: int,
    debug: bool,
) -> str:
    ctx.obj["api_client"].debug_mode = ctx.obj["debug"] or debug
    res_json = (
        ctx.obj["api_client"]
        .get_scope_assessments(
            scope_code,
            page=page_number,
            year_published=year_published,
            latest=latest,
            possibly_extinct=possibly_extinct,
            possibly_extinct_in_the_wild=possibly_extinct_in_the_wild,
        )
        .json
    )
    click.echo(json.dumps(res_json, indent=4))


# ---------------------------------------------------------------------------#
# --- Statistics command group ----------------------------------------------#
# ---------------------------------------------------------------------------#
@redlist_cli.group("statistics", help="Assessment statistics")
@click.pass_context
def statistics(ctx: click.Context): ...


@statistics.command("count", help="A count of all assessed species")
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Debug mode for the request and the response",
)
@click.pass_context
def get_statistics_count(ctx: click.Context, debug: bool) -> str:
    ctx.obj["api_client"].debug_mode = ctx.obj["debug"] or debug
    res_json = ctx.obj["api_client"].get_statistics_count().json
    click.echo(json.dumps(res_json, indent=4))


# ---------------------------------------------------------------------------#
# --- Species stress factors command group ----------------------------------#
# ---------------------------------------------------------------------------#
@redlist_cli.group("stresses", help="Species stress factors")
@click.pass_context
def stresses(ctx: click.Context): ...


@stresses.command("get", help="Species stress factors data")
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Debug mode for the request and the response",
)
@click.pass_context
def get_stresses(ctx: click.Context, debug: bool) -> str:
    ctx.obj["api_client"].debug_mode = ctx.obj["debug"] or debug
    res_json = ctx.obj["api_client"].get_stresses().json
    click.echo(json.dumps(res_json, indent=4))


@stresses.command(
    "get-assessments",
    help="Assessment data related to a specific stress factor by stress code",
)
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Debug mode for the request and the response",
)
@click.option(
    "-s",
    "--scope-code",
    required=False,
    type=int,
    default=None,
    help="Optional geographical assessment scope, defaults to `None` (int)",
)
@click.option(
    "--possibly-extinct-in-the-wild",
    is_flag=True,
    default=None,
    help="Optional indicator of species extinction in the wild status, defaults to `None`",
)
@click.option(
    "--possibly-extinct",
    is_flag=True,
    default=None,
    help="Optional indicator of species extinction status, defaults to `None`",
)
@click.option(
    "--latest",
    is_flag=True,
    default=None,
    help="Optional indicator of whether to get the latest assessments, defaults to `None`",
)
@click.option(
    "-y",
    "--year-published",
    required=False,
    type=str,
    default=None,
    help="Optional publication year number, defaults to `None` (int)",
)
@click.option(
    "-p",
    "--page-number",
    required=False,
    type=str,
    default=None,
    help="Optional page number in the response JSON, defaults to `None` (int)",
)
@click.option(
    "-t",
    "--stress-code",
    required=True,
    type=str,
    help="Species stress factor code (str)",
)
@click.pass_context
def get_stress_assessments(
    ctx: click.Context,
    stress_code: str,
    page_number: int,
    year_published: int,
    latest: bool,
    possibly_extinct: bool,
    possibly_extinct_in_the_wild: bool,
    scope_code: int,
    debug: bool,
) -> str:
    ctx.obj["api_client"].debug_mode = ctx.obj["debug"] or debug
    res_json = (
        ctx.obj["api_client"]
        .get_stress_assessments(
            stress_code,
            page=page_number,
            year_published=year_published,
            latest=latest,
            possibly_extinct=possibly_extinct,
            possibly_extinct_in_the_wild=possibly_extinct_in_the_wild,
            scope_code=scope_code,
        )
        .json
    )
    click.echo(json.dumps(res_json, indent=4))


# ---------------------------------------------------------------------------#
# --- Ecosystems command group ----------------------------------------------#
# ---------------------------------------------------------------------------#
@redlist_cli.group("systems", help="Ecosystems data")
@click.pass_context
def systems(ctx: click.Context): ...


@systems.command("get", help="Species stress factors data")
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Debug mode for the request and the response",
)
@click.pass_context
def get_systems(ctx: click.Context, debug: bool) -> str:
    ctx.obj["api_client"].debug_mode = ctx.obj["debug"] or debug
    res_json = ctx.obj["api_client"].get_systems().json
    click.echo(json.dumps(res_json, indent=4))


@systems.command(
    "get-assessments",
    help="Assessment data related to a specific (eco)system by system code",
)
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Debug mode for the request and the response",
)
@click.option(
    "-s",
    "--scope-code",
    required=False,
    type=int,
    default=None,
    help="Optional geographical assessment scope, defaults to `None` (int)",
)
@click.option(
    "--possibly-extinct-in-the-wild",
    is_flag=True,
    default=None,
    help="Optional indicator of species extinction in the wild status, defaults to `None`",
)
@click.option(
    "--possibly-extinct",
    is_flag=True,
    default=None,
    help="Optional indicator of species extinction status, defaults to `None`",
)
@click.option(
    "--latest",
    is_flag=True,
    default=None,
    help="Optional indicator of whether to get the latest assessments, defaults to `None`",
)
@click.option(
    "-y",
    "--year-published",
    required=False,
    type=str,
    default=None,
    help="Optional publication year number, defaults to `None` (int)",
)
@click.option(
    "-p",
    "--page-number",
    required=False,
    type=str,
    default=None,
    help="Optional page number in the response JSON, defaults to `None` (int)",
)
@click.option(
    "-t", "--system-code", required=True, type=str, help="Ecosystem code (str)"
)
@click.pass_context
def get_system_assessments(
    ctx: click.Context,
    system_code: str,
    page_number: int,
    year_published: int,
    latest: bool,
    possibly_extinct: bool,
    possibly_extinct_in_the_wild: bool,
    scope_code: int,
    debug: bool,
) -> str:
    ctx.obj["api_client"].debug_mode = ctx.obj["debug"] or debug
    res_json = (
        ctx.obj["api_client"]
        .get_system_assessments(
            system_code,
            page=page_number,
            year_published=year_published,
            latest=latest,
            possibly_extinct=possibly_extinct,
            possibly_extinct_in_the_wild=possibly_extinct_in_the_wild,
            scope_code=scope_code,
        )
        .json
    )
    click.echo(json.dumps(res_json, indent=4))


# ---------------------------------------------------------------------------#
# --- Taxa command group ----------------------------------------------------#
# ---------------------------------------------------------------------------#
@redlist_cli.group("taxa", help="Taxa")
@click.pass_context
def taxa(ctx: click.Context): ...


@taxa.group(
    "sis",
    help="Taxa based on Species Information Service (SIS) information",
)
@click.pass_context
def sis(ctx: click.Context): ...


@sis.command(
    "get-assessments",
    help="Assessment data for a specific taxon by Species Identification Service (SIS) system ID",
)
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Debug mode for the request and the response",
)
@click.option("-i", "--sis-id", required=True, type=int, help="SIS ID (int)")
@click.pass_context
def get_taxa_sis_assessments(ctx: click.Context, sis_id: int, debug: bool) -> str:
    ctx.obj["api_client"].debug_mode = ctx.obj["debug"] or debug
    res_json = ctx.obj["api_client"].get_taxa_sis_assessments(sis_id).json
    click.echo(json.dumps(res_json, indent=4))


@taxa.group("scientific-name", help="Requests related to taxa using scientific names")
@click.pass_context
def scientific_name(ctx: click.Context): ...


@scientific_name.command(
    "get-assessments",
    help="Assessment data for a species (or sub-species) by scientific name (in binomial, or trinomial nomenclature)",
)
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Debug mode for the request and the response",
)
@click.option(
    "-b",
    "--subpopulation-name",
    required=False,
    type=str,
    default=None,
    help="Optional subpopulation name (str), defaults to `None` (str)",
)
@click.option(
    "-i",
    "--infra-name",
    required=False,
    type=str,
    default=None,
    help="Optional infraspecific taxon name (str), defaults to `None`",
)
@click.option("-e", "--species-name", required=True, type=str, help="Species name")
@click.option("-g", "--genus-name", required=True, type=str, help="Genus name")
@click.pass_context
def get_taxa_scientific_name_assessments(
    ctx: click.Context,
    genus_name: str,
    species_name: str,
    infra_name: str,
    subpopulation_name: str,
    debug: bool,
) -> str:
    ctx.obj["api_client"].debug_mode = ctx.obj["debug"] or debug
    res_json = (
        ctx.obj["api_client"]
        .get_taxa_scientific_name_assessments(
            genus_name,
            species_name,
            infra_name=infra_name,
            subpopulation_name=subpopulation_name,
        )
        .json
    )
    click.echo(json.dumps(res_json, indent=4))


@taxa.group("kingdom", help="Kingdoms")
@click.pass_context
def kingdom(ctx: click.Context): ...


@kingdom.command("get", help="All kingdom data")
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Debug mode for the request and the response",
)
@click.pass_context
def get_taxa_kingdom(ctx: click.Context, debug: bool) -> str:
    ctx.obj["api_client"].debug_mode = ctx.obj["debug"] or debug
    res_json = ctx.obj["api_client"].get_taxa_kingdom().json
    click.echo(json.dumps(res_json, indent=4))


@kingdom.command(
    "get-assessments", help="Assessment data for a given kingdom by kingdom name"
)
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Debug mode for the request and the response",
)
@click.option(
    "-s",
    "--scope-code",
    required=False,
    type=int,
    default=None,
    help="Optional geographical assessment scope, defaults to `None` (int)",
)
@click.option(
    "--latest",
    is_flag=True,
    default=None,
    help="Optional indicator of whether to get the latest assessments, defaults to `None`",
)
@click.option(
    "-y",
    "--year-published",
    required=False,
    type=str,
    default=None,
    help="Optional publication year number, defaults to `None` (int)",
)
@click.option(
    "-p",
    "--page-number",
    required=False,
    type=str,
    default=None,
    help="Optional page number in the response JSON, defaults to `None` (int)",
)
@click.option("-k", "--kingdom-name", required=True, type=str, help="Kingdom name")
@click.pass_context
def get_taxa_kingdom_assessments(
    ctx: click.Context,
    kingdom_name: str,
    page_number: int,
    year_published: str,
    latest: bool,
    scope_code: str,
    debug: bool,
) -> str:
    ctx.obj["api_client"].debug_mode = ctx.obj["debug"] or debug
    res_json = (
        ctx.obj["api_client"]
        .get_taxa_kingdom_assessments(
            kingdom_name,
            page=page_number,
            year_published=year_published,
            latest=latest,
            scope_code=scope_code,
        )
        .json
    )
    click.echo(json.dumps(res_json, indent=4))


@taxa.group("phylum", help="Phylums")
@click.pass_context
def phylum(ctx: click.Context): ...


@phylum.command("get", help="All phylum data")
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Debug mode for the request and the response",
)
@click.pass_context
def get_taxa_phylum(ctx: click.Context, debug: bool) -> str:
    ctx.obj["api_client"].debug_mode = ctx.obj["debug"] or debug
    res_json = ctx.obj["api_client"].get_taxa_phylum().json
    click.echo(json.dumps(res_json, indent=4))


@phylum.command(
    "get-assessments", help="Assessment data for a given phylum by phylum name"
)
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Debug mode for the request and the response",
)
@click.option(
    "-s",
    "--scope-code",
    required=False,
    type=int,
    default=None,
    help="Optional geographical assessment scope, defaults to `None` (int)",
)
@click.option(
    "--latest",
    is_flag=True,
    default=None,
    help="Optional indicator of whether to get the latest assessments, defaults to `None`",
)
@click.option(
    "-y",
    "--year-published",
    required=False,
    type=str,
    default=None,
    help="Optional publication year number, defaults to `None` (int)",
)
@click.option("-m", "--phylum-name", required=True, type=str, help="Phylum name")
@click.pass_context
def get_taxa_phylum_assessments(
    ctx: click.Context,
    phylum_name: str,
    year_published: str,
    latest: bool,
    scope_code: str,
    debug: bool,
) -> str:
    ctx.obj["api_client"].debug_mode = ctx.obj["debug"] or debug
    res_json = (
        ctx.obj["api_client"]
        .get_taxa_phylum_assessments(
            phylum_name,
            year_published=year_published,
            latest=latest,
            scope_code=scope_code,
        )
        .json
    )
    click.echo(json.dumps(res_json, indent=4))


@taxa.group("class", help="Classes")
@click.pass_context
def class_(ctx: click.Context): ...


@class_.command("get", help="All class data")
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Debug mode for the request and the response",
)
@click.pass_context
def get_taxa_class(ctx: click.Context, debug: bool) -> str:
    ctx.obj["api_client"].debug_mode = ctx.obj["debug"] or debug
    res_json = ctx.obj["api_client"].get_taxa_class().json
    click.echo(json.dumps(res_json, indent=4))


@class_.command(
    "get-assessments", help="Assessment data for a given class by class name"
)
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Debug mode for the request and the response",
)
@click.option(
    "-s",
    "--scope-code",
    required=False,
    type=int,
    default=None,
    help="Optional geographical assessment scope, defaults to `None` (int)",
)
@click.option(
    "--latest",
    is_flag=True,
    default=None,
    help="Optional indicator of whether to get the latest assessments, defaults to `None`",
)
@click.option(
    "-y",
    "--year-published",
    required=False,
    type=str,
    default=None,
    help="Optional publication year number, defaults to `None` (int)",
)
@click.option("-l", "--class-name", required=True, type=str, help="Class name")
@click.pass_context
def get_taxa_class_assessments(
    ctx: click.Context,
    class_name: str,
    year_published: str,
    latest: bool,
    scope_code: str,
    debug: bool,
) -> str:
    ctx.obj["api_client"].debug_mode = ctx.obj["debug"] or debug
    res_json = (
        ctx.obj["api_client"]
        .get_taxa_class_assessments(
            class_name,
            year_published=year_published,
            latest=latest,
            scope_code=scope_code,
        )
        .json
    )
    click.echo(json.dumps(res_json, indent=4))


@taxa.group("order", help="Orders")
@click.pass_context
def order(ctx: click.Context): ...


@order.command("get", help="Data for order taxa")
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Debug mode for the request and the response",
)
@click.pass_context
def get_taxa_order(ctx: click.Context, debug: bool) -> str:
    ctx.obj["api_client"].debug_mode = ctx.obj["debug"] or debug
    res_json = ctx.obj["api_client"].get_taxa_order().json
    click.echo(json.dumps(res_json, indent=4))


@order.command(
    "get-assessments", help="Assessment data for a given order by order name"
)
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Debug mode for the request and the response",
)
@click.option(
    "-s",
    "--scope-code",
    required=False,
    type=int,
    default=None,
    help="Optional geographical assessment scope, defaults to `None` (int)",
)
@click.option(
    "--latest",
    is_flag=True,
    default=None,
    help="Optional indicator of whether to get the latest assessments, defaults to `None`",
)
@click.option(
    "-y",
    "--year-published",
    required=False,
    type=str,
    default=None,
    help="Optional publication year number, defaults to `None` (int)",
)
@click.option("-o", "--order-name", required=True, type=str, help="Phylum name")
@click.pass_context
def get_taxa_order_assessments(
    ctx: click.Context,
    order_name: str,
    year_published: str,
    latest: bool,
    scope_code: str,
    debug: bool,
) -> str:
    ctx.obj["api_client"].debug_mode = ctx.obj["debug"] or debug
    res_json = (
        ctx.obj["api_client"]
        .get_taxa_order_assessments(
            order_name,
            year_published=year_published,
            latest=latest,
            scope_code=scope_code,
        )
        .json
    )
    click.echo(json.dumps(res_json, indent=4))


@taxa.group("family", help="Families")
@click.pass_context
def family(ctx: click.Context): ...


@family.command("get", help="Data for family taxa")
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Debug mode for the request and the response",
)
@click.pass_context
def get_taxa_family(ctx: click.Context, debug: bool) -> str:
    ctx.obj["api_client"].debug_mode = ctx.obj["debug"] or debug
    res_json = ctx.obj["api_client"].get_taxa_family().json
    click.echo(json.dumps(res_json, indent=4))


@family.command(
    "get-assessments", help="Assessment data for a given family by family name"
)
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Debug mode for the request and the response",
)
@click.option(
    "-s",
    "--scope-code",
    required=False,
    type=int,
    default=None,
    help="Optional geographical assessment scope, defaults to `None` (int)",
)
@click.option(
    "--latest",
    is_flag=True,
    default=None,
    help="Optional indicator of whether to get the latest assessments, defaults to `None`",
)
@click.option(
    "-y",
    "--year-published",
    required=False,
    type=str,
    default=None,
    help="Optional publication year number, defaults to `None` (int)",
)
@click.option("-f", "--family-name", required=True, type=str, help="Family name")
@click.pass_context
def get_taxa_family_assessments(
    ctx: click.Context,
    family_name: str,
    year_published: str,
    latest: bool,
    scope_code: str,
    debug: bool,
) -> str:
    ctx.obj["api_client"].debug_mode = ctx.obj["debug"] or debug
    res_json = (
        ctx.obj["api_client"]
        .get_taxa_family_assessments(
            family_name,
            year_published=year_published,
            latest=latest,
            scope_code=scope_code,
        )
        .json
    )
    click.echo(json.dumps(res_json, indent=4))


@taxa.command("possibly-extinct", help="Possibly extinct taxa")
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Debug mode for the request and the response",
)
@click.pass_context
def get_taxa_possibly_extinct(ctx: click.Context, debug: bool) -> str:
    ctx.obj["api_client"].debug_mode = ctx.obj["debug"] or debug
    res_json = ctx.obj["api_client"].get_taxa_possibly_extinct().json
    click.echo(json.dumps(res_json, indent=4))


@taxa.command(
    "possibly-extinct-in-the-wild",
    help="Taxa that are possibly extinct in the wild",
)
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Debug mode for the request and the response",
)
@click.pass_context
def get_taxa_possibly_extinct_in_the_wild(ctx: click.Context, debug: bool) -> str:
    ctx.obj["api_client"].debug_mode = ctx.obj["debug"] or debug
    res_json = ctx.obj["api_client"].get_taxa_possibly_extinct_in_the_wild().json
    click.echo(json.dumps(res_json, indent=4))


# ---------------------------------------------------------------------------#
# --- Threats command group -------------------------------------------------#
# ---------------------------------------------------------------------------#
@redlist_cli.group("threats", help="Species threat factors data")
@click.pass_context
def threats(ctx: click.Context): ...


@threats.command("get", help="Gets all species threat factors data")
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Debug mode for the request and the response",
)
@click.pass_context
def get_threats(ctx: click.Context, debug: bool) -> str:
    ctx.obj["api_client"].debug_mode = ctx.obj["debug"] or debug
    res_json = ctx.obj["api_client"].get_threats().json
    click.echo(json.dumps(res_json, indent=4))


@threats.command(
    "get-assessments",
    help="Assessment data related to a specific threat factor by threat code",
)
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Debug mode for the request and the response",
)
@click.option(
    "-s",
    "--scope-code",
    required=False,
    type=int,
    default=None,
    help="Optional geographical assessment scope, defaults to `None` (int)",
)
@click.option(
    "--possibly-extinct-in-the-wild",
    is_flag=True,
    default=None,
    help="Optional indicator of species extinction in the wild status, defaults to `None`",
)
@click.option(
    "--possibly-extinct",
    is_flag=True,
    default=None,
    help="Optional indicator of species extinction status, defaults to `None`",
)
@click.option(
    "--latest",
    is_flag=True,
    default=None,
    help="Optional indicator of whether to get the latest assessments, defaults to `None`",
)
@click.option(
    "-y",
    "--year-published",
    required=False,
    type=str,
    default=None,
    help="Optional publication year number, defaults to `None` (int)",
)
@click.option(
    "-p",
    "--page-number",
    required=False,
    type=str,
    default=None,
    help="Optional page number in the response JSON, defaults to `None` (int)",
)
@click.option("-t", "--threat-code", required=True, type=str, help="Threat code (str)")
@click.pass_context
def get_threat_assessments(
    ctx: click.Context,
    threat_code: str,
    page_number: int,
    year_published: int,
    latest: bool,
    possibly_extinct: bool,
    possibly_extinct_in_the_wild: bool,
    scope_code: int,
    debug: bool,
) -> str:
    ctx.obj["api_client"].debug_mode = ctx.obj["debug"] or debug
    res_json = (
        ctx.obj["api_client"]
        .get_threat_assessments(
            threat_code,
            page=page_number,
            year_published=year_published,
            latest=latest,
            possibly_extinct=possibly_extinct,
            possibly_extinct_in_the_wild=possibly_extinct_in_the_wild,
            scope_code=scope_code,
        )
        .json
    )
    click.echo(json.dumps(res_json, indent=4))


# ---------------------------------------------------------------------------#
# --- Use and trade command group -------------------------------------------#
# ---------------------------------------------------------------------------#
@redlist_cli.group("use-and-trade", help="Species use and trade factors data")
@click.pass_context
def use_and_trade(ctx: click.Context): ...


@use_and_trade.command("get", help="Gets all species use and trade factors data")
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Debug mode for the request and the response",
)
@click.pass_context
def get_use_and_trade(ctx: click.Context, debug: bool) -> str:
    ctx.obj["api_client"].debug_mode = ctx.obj["debug"] or debug
    res_json = ctx.obj["api_client"].get_use_and_trade().json
    click.echo(json.dumps(res_json, indent=4))


@use_and_trade.command(
    "get-assessments",
    help="Assessment data related to a specific use and trade factor by code",
)
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Debug mode for the request and the response",
)
@click.option(
    "-s",
    "--scope-code",
    required=False,
    type=int,
    default=None,
    help="Optional geographical assessment scope, defaults to `None` (int)",
)
@click.option(
    "--possibly-extinct-in-the-wild",
    is_flag=True,
    default=None,
    help="Optional indicator of species extinction in the wild status, defaults to `None`",
)
@click.option(
    "--possibly-extinct",
    is_flag=True,
    default=None,
    help="Optional indicator of species extinction status, defaults to `None`",
)
@click.option(
    "--latest",
    is_flag=True,
    default=None,
    help="Optional indicator of whether to get the latest assessments, defaults to `None`",
)
@click.option(
    "-y",
    "--year-published",
    required=False,
    type=str,
    default=None,
    help="Optional publication year number, defaults to `None` (int)",
)
@click.option(
    "-p",
    "--page-number",
    required=False,
    type=str,
    default=None,
    help="Optional page number in the response JSON, defaults to `None` (int)",
)
@click.option(
    "-u",
    "--use-and-trade-code",
    required=True,
    type=str,
    help="Use and trade code (str)",
)
@click.pass_context
def get_use_and_trade_assessments(
    ctx: click.Context,
    use_and_trade_code: str,
    page_number: int,
    year_published: int,
    latest: bool,
    possibly_extinct: bool,
    possibly_extinct_in_the_wild: bool,
    scope_code: int,
    debug: bool,
) -> str:
    ctx.obj["api_client"].debug_mode = ctx.obj["debug"] or debug
    res_json = (
        ctx.obj["api_client"]
        .get_use_and_trade_assessments(
            use_and_trade_code,
            page=page_number,
            year_published=year_published,
            latest=latest,
            possibly_extinct=possibly_extinct,
            possibly_extinct_in_the_wild=possibly_extinct_in_the_wild,
            scope_code=scope_code,
        )
        .json
    )
    click.echo(json.dumps(res_json, indent=4))
