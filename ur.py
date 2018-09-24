#!/usr/bin/python3

class UsageRecord:
    def __init__(self, jobId, user, startTime, endTime, serviceId):
        self.jobId = jobId
        self.user = user
        self.startTime = startTime
        self.endTime = endTime
        self.serviceId = serviceId

def parse_usage_record(json):
    ur = UsageRecord(
        json["jobId"],
        json["user"],
        int(json["startTime"]),
        int(json["endTime"]),
        json["service"])

    return(ur)
