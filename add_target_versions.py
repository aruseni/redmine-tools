# -*- coding: utf-8 -*-

#
#
# Redmine target version creator v0.1
#
# Author: aruseni <aruseni.magiku@gmail.com>
# Licence: CC BY 3.0
# (https://creativecommons.org/licenses/by/3.0/)
#
#

import sys
import json
import httplib
import urllib
import datetime

redmine_host = "redmine.amazingserver.com"
redmine_project_name = "coolproject"
redmine_api_key = "put_your_api_key_here"

class VersionCreator():
    def send_request(self, method, url, data=None):
        http_headers = {
            "Content-Type": "application/json",
            "X-Redmine-API-Key": redmine_api_key,
        }

        connection = httplib.HTTPSConnection(redmine_host, timeout=5)

        connection.request(
            method,
            url,
            json.dumps(data) if data else None,
            http_headers
        )

        response = connection.getresponse()

        return response.read()

    def create(self, first_version_end_date, number_of_versions):
        for i in xrange(number_of_versions):
            if i == 0:
                version_end_date = first_version_end_date
            else:
                version_end_date = (
                    first_version_end_date + datetime.timedelta(weeks=i)
                )
            version_name = version_end_date.strftime("%Y%U")
            version_description = (
                u"План работ на %(week)d-ю неделю %(year)s года" % {
                    "week": int(version_end_date.strftime("%U")),
                    "year": version_end_date.strftime("%Y"),
                }
            )

            print "Creating version %s" % version_name

            self.send_request(
                "POST",
                "/projects/%s/versions.json" % redmine_project_name,
                {
                    "version": {
                        "name": version_name,
                        "status": "open",
                        "sharing": "system",
                        "due_date": version_end_date.strftime("%Y-%m-%d"),
                        "description": version_description,
                    }
                }
            )

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python add_target_versions.py [date] [number]")
        print("Replace [date] by the end date (Sunday, e.g. 2014-01-05)")
        print("of the first target version to create.")
        print("Replace [number] by the number of target versions.")
        exit()

    first_version_end_date = datetime.datetime.strptime(
        sys.argv[1],
        "%Y-%m-%d"
    )
    number_of_versions = int(sys.argv[2])

    if first_version_end_date.strftime("%w") != "0":
        print("Not a Sunday")
        exit()

    VersionCreator().create(first_version_end_date, number_of_versions)
