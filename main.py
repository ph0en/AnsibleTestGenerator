#!/usr/bin/env python3

import oyaml as yaml
import os
import pytest

tasks_path = '/<path>/<to>/<dir>/<with>/<.yml>/<files>'


def check_yum(files_path):
    files = sorted(os.listdir(files_path))
    lst = []
    for file in [f for f in files if os.path.isfile(os.path.join(files_path, f)) and f.endswith('.yml')]:
        for task in yaml.safe_load(open(os.path.join(files_path, file))):
            if 'yum' and 'vars' in task:
                item_to_append = task['yum']
                item_to_append['name'] = task['vars'][item_to_append['name'].split()[1]]
                lst.append(item_to_append)
            elif 'yum' in task:
                lst.append(task['yum'])
    return lst


def check_file(files_path):
    files = sorted(os.listdir(files_path))
    lst = []
    for file in [f for f in files if os.path.isfile(os.path.join(files_path, f)) and f.endswith('.yml')]:
        for task in yaml.safe_load(open(os.path.join(files_path, file))):
            if 'file' in task:
                lst.append(task['file'])
    return lst


files_list = check_file(tasks_path)
packages_list = check_yum(tasks_path)


@pytest.mark.parametrize('yum_task', packages_list)
def test_pkg(host, yum_task):
    if type(yum_task['name']) == str:
        package = host.package(yum_task['name'])
        if 'state' in yum_task:
            if yum_task['state'] == 'absent':
                assert not package.is_installed
            elif yum_task['state'] == 'present' or yum_task['state'] == 'latest':
                assert package.is_installed
        else:
            assert package.is_installed
    elif type(yum_task['name']) == list:
        for i in yum_task['name']:
            package = host.package(i)
            if 'state' in yum_task:
                if yum_task['state'] == 'absent':
                    assert not package.is_installed
                elif yum_task['state'] == 'present' or yum_task['state'] == 'latest':
                    assert package.is_installed
            else:
                assert package.is_installed


@pytest.mark.parametrize('file_task', files_list)
def test_file(host, file_task):
    file = host.file(file_task['path'])
    if 'state' in file_task:
        if file_task['state'] == 'absent':
            assert not file.exists
        else:
            assert file.exists
