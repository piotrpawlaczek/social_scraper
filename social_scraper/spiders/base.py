from scrapy.spider import Spider
from scrapy.http import TextResponse, Request


class SocialSpider(Spider):
    """
    The social spider is new api-like type,
    adapted to use neat scrapy features
    like stats, scheduler, cute abstraction layer, etc
    """
    name = None  # spider name
    profile = None  # structure with user profile data

    def __init__(self, username=None, *args, **kwargs):
        """
        Here we are be able to pass also a list of users.
        This will add more work for spider ( worker )
        """
        super(SocialSpider, self).__init__(*args, **kwargs)
        if username:
            self.start_usernames = [ username ]

    def start_requests(self):
        """
        Process initial data, this method is run once and we
        are safe to use gen
        """
        for username in self.start_usernames:
            yield self._make_request_from_username(username)

    def api_call(self, username):
        """
        Each `social` spider is oblidged to define this method
        :: return dict, with `status_code`, `content` and `url`
        """
        raise NotImplementedError

    def _make_request_from_username(self, username):
        """
        Helper func, run spider api_call and return reponse
        """
        call = self.api_call(username)
        return self._build_reponse(call)

    def _build_reponse(self, call, callback=None, errback=None):
        """
        `Scrapy.engine` expects from spider `Response` or `Request` obj.
        As we use api calls directly we miss them. Therefore, we do build
        and return tuned or fake `Response` obj to cheat scarpy a lille bit.
        """
        r = TextResponse(str(call['url']),
                status=call['status_code'],
                body=call['content'],
                encoding='utf-8', # utf-8 is standard for json response
                request=Request(str(call['url']), method='GET')
        )
        r.dont_filter = True
        r.priority = 0
        r.method = 'GET'
        r.callback = callback
        r.errback = errback
        return r
