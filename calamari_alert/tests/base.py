from testtools import TestCase
from testtools.content import Content
from testtools.content_type import UTF8_TEXT
from testtools.matchers import Equals


class TestSillySquareServer(TestCase):

    def __init__(self, *args, **kwargs):
        super(TestSillySquareServer, self).__init__(*args, **kwargs)
        self.server = self.useFixture()

    def setUp(self):
        super(TestSillySquareServer, self).setUp()
        self.addCleanup(self.attach_log_file)

    def attach_log_file(self):
        self.addDetail(
            'log-file',
            Content(UTF8_TEXT,
                    lambda: open(self.server.logfile, 'r').readlines()))

    def test_server_is_cool(self):
        self.assertThat(self.server.temperature, Equals("cool"))

    def test_square(self):
        self.assertThat(self.server.silly_square_of(7), Equals(49))