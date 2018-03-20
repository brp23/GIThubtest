from github import Github
from github import GithubException
import sys, argparse
  
g = Github("your token")
user_login = ''
email_id = ''


def check_arg(args=None):
    parser = argparse.ArgumentParser(description='Get username and email as arguments')
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
    check_user(user_login)

def check_user(username):
  try:
    q = g.get_user(login=username)
    user_login_found = q.login
    org = g.get_organization( "sasiorg" )
    teams = org.get_teams()
    team = [t for t in teams if t.name == 'all'][0]
    print "public members of", org.login, ":"
    for member in org.get_public_members():
      print "   ", member.login, "<--- HERE" if member.login == user_login_found else ""
    print org.login, "has_in_members", user_login_found, "?", org.has_in_members( q )
    print org.login, "has_in_public_members", user_login_found, "?", org.has_in_public_members( q )
    if org.has_in_members( q ):
      print("user found, the user already exists in the organization")
    else:
      print("user account exists in github but not added to org")
      t.add_membership( q , role="member")
      #t.add_to_members( q )
      #org.invitations( q )
  except GithubException as e:
    if (e.status == 404):
      print("user not found") 
    else:
      print(e)

if __name__ == '__main__':
    check_arg(sys.argv[1:])
