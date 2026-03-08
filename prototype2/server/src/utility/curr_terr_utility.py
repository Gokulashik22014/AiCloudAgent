import os


CURR_TERRAFORM_PATH=os.path.join(os.getcwd(),"server","curr_terraform")
TEMPLATE_PATH=os.path.join(os.getcwd(),"server","terraform_templates")

def add_to_curr_terraform(value:str):
    print(value)
    if value not in ("ec2","s3"):
        print("The specified path does not exist")
        return False
    temp=os.path.join(TEMPLATE_PATH,value)
    folders_to_change=["main.tf","variables.tf"]
    for i in folders_to_change:
        with open(os.path.join(CURR_TERRAFORM_PATH,i),'a') as dest_file:
            dest_file.write("\n")
            with open(os.path.join(temp,i),'r') as src_file:
                dest_file.write(src_file.read())
    return True