#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_own_module

short_description: This module can be create file with content.

version_added: "1.0.0"

description: This module can be create file with content.

options:
    path:
        description: Name of the file to be created.
        required: true
        type: str
    content:
        description: Contents in the target file
        required: true
        type: str

extends_documentation_fragment: []

author:
    - Andrey Shitov (@ShitovAndrey)
'''

EXAMPLES = r'''
# Create a content file
- name: Test filw with a content
  my_own_namespace.yandex_cloud_elk.my_own_module:
    path: "/tmp/my_own_module.txt"
    content: "Hello Netology!"
'''

RETURN = r'''
# These are examples of possible return values.
target_path:
    description: Path to the file that will be created.
    type: str
    returned: always
    sample: '/tmp/my_own_module.txt'
'''

from ansible.module_utils.basic import AnsibleModule
import os
import tempfile
import hashlib

tmp_file_path = ""

def check_exist_file(file_path):
    file_status = False
    file_status = os.path.isfile(file_path)
    return file_status

def create_tmp_file(file_content):
    return_tmp_file_path = "None"
    tmp_file_path = tempfile.NamedTemporaryFile(delete=False)
    return_tmp_file_path = tmp_file_path.name

    with open(return_tmp_file_path, "w") as tmp_file:
      tmp_file.write(file_content)

    return return_tmp_file_path

def diff_check_between_files(file_path, tmp_file_path):
    diff_status = True
    md5_old_file = hashlib.md5()
    md5_new_file = hashlib.md5()
    
    with open(file_path,'rb') as file_old:
      chunk = 0
      while chunk != b'':
        chunk = file_old.read(1024)
        md5_old_file.update(chunk)

    with open(tmp_file_path,'rb') as file_new:
      chunk = 0
      while chunk != b'':
        chunk = file_new.read(1024)
        md5_new_file.update(chunk)

    if md5_old_file.hexdigest() == md5_new_file.hexdigest():
      diff_status = False
    else:
      diff_status = True
    
    return diff_status

def rename_tmp_file_to_target(file_path, tmp_file_path):
    os.rename(tmp_file_path, file_path)

def delete_tmp_file(tmp_file_path):
    os.remove(tmp_file_path)

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        path=dict(type='str', required=True),
        content=dict(type='str', required=True)
    )

    result = dict(
        changed=False,
        target_path=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    file_path = module.params['path']
    file_content = module.params['content']
    is_changed = False

    if check_exist_file(file_path):
        tmp_file_path = create_tmp_file(file_content)
        if diff_check_between_files(file_path, tmp_file_path):
          rename_tmp_file_to_target(file_path, tmp_file_path)
          is_changed = True
    else:
        tmp_file_path = create_tmp_file(file_content)
        rename_tmp_file_to_target(file_path, tmp_file_path)
        is_changed = True
    
    if check_exist_file(tmp_file_path):
        delete_tmp_file(tmp_file_path)
    
    result['target_path'] = module.params['path']
    result['changed'] = is_changed

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()