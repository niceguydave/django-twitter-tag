from django import template
from templatetag_sugar.parser import Optional, Constant, Name, Variable
from templatetag_sugar.register import tag
import ttp
import twitter


register = template.Library()


@tag(register, [Constant("for"), Variable(), Constant("as"), Name(),
                Optional([Constant("with"), Variable('replies')]),
                Optional([Constant("limit"), Variable('limit')])])
def get_tweets_new(context, username, asvar, replies=False, limit=None):
    p = ttp.Parser()
    tweets = []
    user_last_tweets = twitter.Api().GetUserTimeline(id=username, include_rts=True, include_entities=True)

    for status in user_last_tweets:
        if not replies and status.GetInReplyToUserId() is not None:
            continue

        tweet = status.AsDict()
        tweet['html'] = p.parse(tweet['text']).html
        tweets.append(tweet)

    if limit:
        tweets = tweets[:limit]

    context[asvar] = tweets

    return ""