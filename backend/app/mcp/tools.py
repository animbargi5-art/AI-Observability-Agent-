from enum import Enum


class MCPTool(str, Enum):

    # Metrics
    LIST_METRICS = "signoz_list_metrics"
    QUERY_METRICS = "signoz_query_metrics"
    TOP_METRICS = "signoz_get_top_metrics"
    METRIC_USAGE = "signoz_check_metric_usage"
    METRIC_CARDINALITY = "signoz_check_metric_cardinality"

    # Logs
    SEARCH_LOGS = "signoz_search_logs"
    AGGREGATE_LOGS = "signoz_aggregate_logs"

    # Traces
    SEARCH_TRACES = "signoz_search_traces"
    AGGREGATE_TRACES = "signoz_aggregate_traces"
    TRACE_DETAILS = "signoz_get_trace_details"

    # Services
    LIST_SERVICES = "signoz_list_services"
    TOP_OPERATIONS = "signoz_get_service_top_operations"

    # Alerts
    LIST_ALERTS = "signoz_list_alerts"
    LIST_ALERT_RULES = "signoz_list_alert_rules"
    GET_ALERT = "signoz_get_alert"

    # Dashboards
    LIST_DASHBOARDS = "signoz_list_dashboards"
    GET_DASHBOARD = "signoz_get_dashboard"

    # Query Builder
    EXECUTE_QUERY = "signoz_execute_builder_query"

    # Documentation
    SEARCH_DOCS = "signoz_search_docs"
    FETCH_DOC = "signoz_fetch_doc"