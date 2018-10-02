#!/bin/bash

# The script is supposed to be called by cron to maintain the usage
# records exposed by the application

KEY="/etc/apache2/mellon/proxy_west_life.ics.muni.cz.key"

./create_usage_record.py $KEY << EOF
{
    "status" : "success",
    "data" : [
        { 
            "jobId" : "job_1",
            "user" : "kouril",
            "startTime" : "1536173048",
            "endTime" : "1536173248",
            "service" : "makac"
        },
        {
            "jobId" : "job_2",
            "user" : "ljocha",
            "startTime" : "1536173000",
            "endTime" : "1536173047",
            "service" : "makac"
        }
    ]
}
EOF
