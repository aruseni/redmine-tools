# -*- coding: utf-8 -*-

#
#
# Redmine target version shift v0.1
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

redmine_host = "redmine.amazingserver.com"
redmine_project_name = "coolproject"
redmine_assignee_id = 100500
redmine_api_key = "put_your_api_key_here"

class Shifter():
    def __init__(self, target_version):
        self.from_version = target_version

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

    def shift(self):
        versions = self.send_request(
            "GET",
            "/projects/%s/versions.json" % redmine_project_name
        )

        version_names_by_id = {
            v["id"] : v["name"] for v in json.loads(versions)["versions"]
        }

        version_ids_by_name = {
            version_names_by_id[k] : k for k in version_names_by_id
        }

        self.from_version_id = version_ids_by_name[self.from_version]

        query_string = urllib.urlencode({
            "project_id": redmine_project_name,
            "assigned_to_id": redmine_assignee_id,
            "fixed_version_id": "*",
            "limit": 100,
        })

        issues = self.send_request(
            "GET",
            "/issues.json?%s" % query_string
        )

        for issue in json.loads(issues)["issues"]:
            current_version = issue["fixed_version"]["id"]

            if issue["fixed_version"]["id"] < self.from_version_id:
                continue

            next_version = current_version + 1

            print(
                ("Shifting #%(id)s from %(current_version)s "
                 "to %(next_version)s") % {
                    "id": issue["id"],
                    "current_version": issue["fixed_version"]["name"],
                    "next_version": version_names_by_id[next_version],
                }
            )

            self.send_request(
                "PUT",
                "/issues/%s.json" % issue["id"],
                {
                    "issue": {
                        "fixed_version_id": next_version,
                    }
                }
            )

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python redmine_tv_shift.py [target_version]")
        print("Replace [target_version] by the target version")
        print("from which the shift should start.")
        exit()
    Shifter(sys.argv[1]).shift()
