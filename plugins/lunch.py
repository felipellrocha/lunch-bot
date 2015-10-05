from slackbot.bot import respond_to
from slackbot.bot import listen_to

from collections import defaultdict

votes_count = defaultdict(int)
votes_users = defaultdict(list)


@listen_to('!restart')
def start(message):
    global votes_count
    global votes_users

    votes_count = defaultdict(int)
    votes_users = defaultdict(list)

    message.reply('Voting process restarted!')

@listen_to('!vote (.*)')
def add_vote(message, vote_list):
    """
        Comma separated votes.
        Users can vote on multiple places.
        As such:

        !vote Agora,mediterranea,Corner bakery
    """
    global votes_count
    global votes_users

    buf = '\n'
    buf += 'Voted for:\n'
    user = message._client.users.get(message._body['user']).get('name')
    for vote in vote_list.split(','):
        vote = vote.lower().strip()
        if not vote in votes_users[user]:
            buf += '%s (+1)\n' % vote
            votes_count[vote] += 1
            votes_users[user].append(vote)
        else:
            buf += '%s (DOUBLE VOTE)\n' % vote

    message.reply(buf)

@listen_to('!status')
def status(message):
    global votes_count
    global votes_users

    buf = '\n'
    buf += 'Here is the current vote status:\n'
    for vote, count in votes_count.iteritems():
        buf += '%s: %d\n' % (vote, count)

    message.reply(buf)
