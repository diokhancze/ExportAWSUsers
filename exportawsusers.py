#!/usr/bin/env python3

import boto3
import botocore
import sys

KEY = ''
SECRET = ''
MAXITEMS = 100


def get_iam_connection():
    """
    Get a connection to IAM region.
    """
    try:
        return boto3.client(
            'iam',
            aws_access_key_id=KEY,       # ADD YOUR OWN AWS API KEY
            aws_secret_access_key=SECRET # ADD YOUR OWN AWS SECRET KEY
        )

    except botocore.exceptions.ClientError as e:
        print(e.response['Error']['Message'])
        sys.exit(1)


def get_iam_users():
    """
    Return a list of IAM user accounts. Get the users in batches.
    """
    users = []
    more = True
    marker = ''

    while more is True:
        u = {}
        if marker == '':
            u = conn.list_users(MaxItems=MAXITEMS)
        else:
            u = conn.list_users(Marker=marker, MaxItems=MAXITEMS)

        more = u.get('IsTruncated')
        marker = u.get('Marker')
        users.extend(u['Users'])

    return users


def get_iam_user_groups(user):
    """
    Return a list of groups of which the IAM user is a member. Get the groups
    in batches.
    """
    groups = []
    more = True
    marker = ''

    while more is True:
        g = {}
        if marker == '':
            g = conn.list_groups_for_user(UserName=user, MaxItems=MAXITEMS)
        else:
            g = conn.list_groups_for_user(UserName=user, Marker=marker, MaxItems=MAXITEMS)

        more = g.get('IsTruncated')
        marker = g.get('Marker')
        groups.extend([f['GroupName'] for f in g['Groups']])

    return groups


def get_iam_key_last_used(key):
    """
    Return the last used date of the specified key.
    """
    last_used = conn.get_access_key_last_used(AccessKeyId=key)
    alu = last_used.get('AccessKeyLastUsed')

    if alu.get('LastUsedDate') is None:
        return 'Never'
    else:
        return str(alu.get('LastUsedDate'))


def get_iam_user_keys(user):
    """
    Return a list of access keys which belong to the IAM user. Get the keys in
    batches.
    """
    keys = []
    more = True
    marker = ''

    while more is True:
        k = {}
        if marker == '':
            k = conn.list_access_keys(UserName=user, MaxItems=MAXITEMS)
        else:
            k = conn.list_access_keys(UserName=user, Marker=marker, MaxItems=MAXITEMS)

        more = k.get('IsTruncated')
        marker = k.get('Marker')
        key_list = [l['AccessKeyId'] for l in k['AccessKeyMetadata']]
        for key in key_list:
            last_used = get_iam_key_last_used(key)
            keys.append((key, last_used[:10]))

    return keys


def write_users(users):
    """
    Write the user details to a file.
    """
    fn = 'iam_user_accounts.txt'
    fh = open(fn, 'w')
    fh.write('IAM User Accounts\n')
    fh.write('=================\n')
    fh.write('\n')

    for user in users:
        name = user.get('UserName', 'No Name')
        groups = get_iam_user_groups(name)
        keys = get_iam_user_keys(name)
        created = str(user.get('CreateDate'))
        last_login = str(user.get('PasswordLastUsed', 'Never'))

        fh.write('Username: {0}\n'.format(name))
        fh.write('Created: {0}\n'.format(created[:10]))
        fh.write('Last Login: {0}\n'.format(last_login[:10]))
        fh.write('Groups: {0}\n'.format(', '.join(groups)))
        fh.write('Keys: {0}\n'.format(', '.join(['{0} ({1})'.format(k[0], k[1]) for k in keys])))
        fh.write('\n')

    fh.close()


if __name__ == '__main__':
    conn = get_iam_connection()
    users = get_iam_users()
    write_users(users)
