import json
import jinja2

def read_cridr():
    res = json.load(open("plan-secgroup.plan"))
    for item in res['planned_values']['root_module']['child_modules'][0]['resources']:
        if 'cidr_blocks' in item['values']:
            print(item['values']['cidr_blocks'])

def jsonload(file):
    res = json.load(open(file))
    return res

#return all resources in the plan
def getplannedchild(res):
    child_resources= res['planned_values']['root_module']['child_modules']
    return child_resources

#return specified type of resources
def generate_dictionary_for_resource(res,type_resource):
    resouces = []
    for i in range(len(res)):
        for resource in res[i]['resources']:
          if resource['type'] == type_resource:
            resouces.append(resource['values'])
    #print(json.dumps(rule, indent=4))
    return resouces

#read template jinnja and pass variables write an html file
def read_template( filej2, variables):
    templateLoader = jinja2.FileSystemLoader(searchpath=".")
    templateEnv = jinja2.Environment(loader=templateLoader)
    template = templateEnv.get_template(filej2)
    outputText = template.render(rule= variables)
    return outputText

def write_file(content, filedest):
    with open(filedest, "w") as file:
        file.write(content)


if __name__ == '__main__':
    res =jsonload("plan-secgroup.plan")
    child_resource = getplannedchild(res)
    dictionary= generate_dictionary_for_resource(child_resource,'aws_security_group_rule')
    secgrouprulehtml= read_template('templateHtml.html.j2', dictionary)
    write_file(secgrouprulehtml,'myfile.html')