
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

GET /report_id

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