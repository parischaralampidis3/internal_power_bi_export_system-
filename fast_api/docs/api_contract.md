
# Reports Endpoint Contract

GET /reports

Response:

{
    "reports":[
        {
            "report_id": "string",
            "title": "string"
        }
    ]
}


# Pages Endpoint Contract

GET /pages/{report_id}

Response:
{
    "pages":[
        {
            "page_name":"string",
            "page_id":"string"
            "is_default": "boolean" 
        }
    ]
}


# Filters Endpoint Contract 

GET /filters/{report_id}

Response:
{
    "filters":[
            "filter_label":"string",
            "column_name":"string",
            "allowed_values":"array",
            "default_values":"string|null"
    ]
}