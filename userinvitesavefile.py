#!/usr/bin/python
# -*- coding: utf-8 -*-

from github import Github
from github import GithubException
import os, sys, argparse

g = Github("your token")
user_login = ''
email_id = ''


def check_arg(args=None):
    parser = argparse.ArgumentParser(description='Get username and email as arguments')
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-i", "--invite", action="store_true")
    group.add_argument("-r", "--remove", action="store_true")
    group.add_argument("-a", "--getmembers", action="store_true")
    parser.add_argument('-u', '--user_id',
                        help='Enter a valid username',
                        required='True',
                        default='testxtetx')
    parser.add_argument('-e', '--email_id',
                        help='email id of the user',
                        default='abc@xyz.com')

    results = parser.parse_args(args)
    user_login = results.user_id
    email_id = results.email_id
    if results.invite:
        invite_user(user_login)
    elif results.remove:
        remove_user(user_login)
    elif results.getmembers:
        user_list()


def invite_user(username):
    try:
        u_name = g.get_user(login=username)
        user_login_found = u_name.login
        org = g.get_organization("kushalIt")
        teams = org.get_teams()
        # team = [t for t in teams if t.name == 'all'][0]
        for t in teams:
            if t.name == "team name ":
                print(t.name)
                print("public members of", org.login, ":")
                for member in org.get_public_members():
                    print("   ", member.login, "<--- HERE" if member.login == user_login_found else "")
                print(org.login, "has_in_members", user_login_found, "?", org.has_in_members(u_name))
                print(org.login, "has_in_public_members", user_login_found, "?", org.has_in_public_members(u_name))
                if org.has_in_members(u_name):
                    print("user found, the user already exists in the organization")
                else:
                    print("user account exists in github but not added to org")
                    try:
                        t.add_membership(u_name, role="member")
                        # t.add_to_members( u_name )
                        # org.invitations( u_name )
                    except GithubException as e1:
                        print(e1)
            else:
                print("skippedadding to team", t.name)
    except GithubException as e2:
        if (e2.status == 404):
            print("user not found")
        else:
            print(e2)


def remove_user(username):
    try:
        u_name = g.get_user(login=username)
        user_login_found = u_name.login
        org = g.get_organization("org-name")
        remove_member = org.remove_from_members(u_name)
        print("user removed from org", user_login_found)
        print(remove_member)
    except GithubException as e3:
        if (e3.status == 404):
            print("user not found")
        else:
            print(e3)


def user_list():
    org = g.get_organization("org")
    with open("gitautomate.txt", "a") as fil:
        try:
            fil.write("Existing Member list\n")
            for m in org.get_members(role="members"):
                fil.write("User-id is :" + m.login + "\t" + "Profile_name is :" + m.name + "\n")
        except GithubException as e4:
            if (e4.status == 404):
                print("error")
            else:
                print(e4)
        fil.write("Organization Repository list\n")
        for repos in org.get_repos():
            fil.write("Repository_Name:" + repos.name + "\n")
    fil.close()


if __name__ == '__main__':
    check_arg (sys.argv[1:])
