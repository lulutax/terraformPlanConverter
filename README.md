## Docs

   **--plan**           Required, specify terraform plan 

   **--template**   Optional, specify template html, default="templates/templateText.txt.j2"

   **--output**         Optional, specify type of output, choose by txt or html, default="txt"

   **--checkmode**      Optional, if "yes" it will check if there are only changes in the plan and return true, default="no"
    
## Usage
*example:*

    python .\main.py  --plan pathofterraformplan/example.plan 

