import logging
import os
import jinja2
from bs4 import BeautifulSoup


class Converter:

    # read template jinnja and pass variables write an html file
    def read_template(self, dictionary, template):
        _file = str(template)
        try:
            filePath = f"{os.path.sep}".join(_file.split(os.path.sep)[0:-1])
            templateLoader = jinja2.FileSystemLoader(filePath)
            templateEnv = jinja2.Environment(loader=templateLoader)
            template = templateEnv.get_template(_file.split(os.path.sep)[-1])
            outputText = template.render(resource=dictionary)
            return outputText
        except jinja2.exceptions.TemplateNotFound as e:
            logging.error(f"Template {_file} not found ")
            raise
        except jinja2.exceptions.TemplateSyntaxError as syntaxerror:
            raise syntaxerror

    def write_file(self, content, filedest):
        with open(filedest, "w") as file:
            file.write(content)
            return filedest

    def convertHtml(self, dictionary, template):

        if template[-7:-3] == "html":
            secgrouprulehtml = self.read_template(dictionary, template)
            soup = BeautifulSoup(secgrouprulehtml, "html.parser")
            prettyhtml = soup.prettify()
            return self.write_file(prettyhtml, "myfile.html")
        else:
            raise Exception("Template wrong")

    def convertTxt(self, dictionary, template):

        if template[-6:-3] == "txt":
            secgroupruletxt = self.read_template(dictionary, template)
            return self.write_file(secgroupruletxt, "myfile.txt")
        else:
            raise Exception("Template wrong")
