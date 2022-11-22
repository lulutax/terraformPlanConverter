import json
import logging
import re

logging.basicConfig(level=logging.INFO)


class Plan:
    def __init__(self):
        self.res = ""

    def getRes(self):
        return self.res

    def setRes(self, res):
        self.res = res

    def jsonload(self, plan):
        try:
            self.res = json.load(open(plan))
            return self.res
        except FileNotFoundError:
            logging.exception("File not found!")
            raise
        except json.decoder.JSONDecodeError as e:
            logging.exception("Failed to load")
            raise

    def recursive_child(self, res):
        for item in res:
            if "child_modules" in item:
                return self.recursive_child(item["child_modules"])
        return res

    # return all resources in the plan
    def getplannedchild(self):
        try:
            return self.recursive_child(
                self.res["planned_values"]["root_module"]["child_modules"]
            )
        except KeyError as e:
            logging.exception("No key " + (str(e)) + "found into plan")
            raise

    # return True if there are only changes
    def getchangedchild(self, res_change):
        listofchanges = res_change["resource_changes"]
        for resource in listofchanges:
            if resource["change"]["actions"][0] == "create" and (
                resource["type"] == "aws_security_group"
                or resource["type"] == "aws_security_group_rule"
            ):
                return False
        return True

    # concact the action to the security group
    def getchangedchildlist(self, dict, res_change):
        for item in dict:
            for resource in res_change:
                try:
                    if (
                        resource["type"] == "aws_security_group"
                        and resource["index"] == item
                    ):
                        dict[item].insert(0, {"action": resource["change"]["actions"]})

                except KeyError as e:
                    logging.exception(e)
                    raise e
        return dict

    # return specified type of resources
    def generate_dictionary_for_resource(self, child):
        resources = {}
        # First: insert as key of dict the name of security group
        for i in range(len(child)):
            for resource in child[i]["resources"]:
                if resource["type"] == "aws_security_group":
                    resources.update({resource["index"]: []})

        # Secodn: if name of rule match with the key (namesecgroup_nomerule) insert as value the rule
        for i in range(len(child)):
            for resource in child[i]["resources"]:
                if resource["type"] == "aws_security_group_rule":
                    index = re.search(r"^([a-z]+\d*)", resource["index"])
                    resources[index.group(0)].append(
                        {"name": resource["index"]} | resource["values"]
                    )
        return resources

    def extractDictionary(self, check):
        try:
            if check == "yes":
                return self.getchangedchild(self.res)
            ## sys.exit(0)
            ## return true if there are only changes and not create
            else:
                child_resource = self.getplannedchild()
                dictionary = self.generate_dictionary_for_resource(child_resource)

                if len(dictionary) == 0:
                    return "No Resources"
                result = self.getchangedchildlist(
                    dictionary, self.res["resource_changes"]
                )
                return result
        except Exception as e:
            logging.exception(e)
            raise e
