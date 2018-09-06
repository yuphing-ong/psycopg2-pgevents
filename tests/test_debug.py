import logging
from pytest import raises

from psycopg2_pgevents import debug
from psycopg2_pgevents.debug import set_debug, log


class TestDebug:
    def test_set_debug_disabled(self):
        debug._DEBUG_ENABLED = True
        set_debug(False)

        assert (debug._DEBUG_ENABLED == False)

    def test_set_debug_enabled(self):
        debug._DEBUG_ENABLED = False
        set_debug(True)

        assert (debug._DEBUG_ENABLED == True)

    def test_log_invalid_category(self, log_capture):
        with raises(ValueError):
            log('foo', category='warningwarningwarning')

        logs = log_capture.actual()
        assert (len(logs) == 0)

    def test_log_debug_disabled(self, log_capture):
        set_debug(False)
        log('foo')

        logs = log_capture.actual()
        assert (len(logs) == 0)

    def test_log_info(self, log_capture):
        log('foo')

        logs = log_capture.actual()

        assert (len(logs) == 1)
        assert (('psycopg2', 'INFO', 'foo') == logs.pop())

    def test_log_error(self, log_capture):
        log('foo', category='error')

        logs = log_capture.actual()

        assert (len(logs) == 1)
        assert (('psycopg2', 'ERROR', 'foo') == logs.pop())

    def test_log_args(self, log_capture):
        log('foo %s %s %d', 'bar', 'baz', 1)
        log(
            'foo %(word1)s %(word2)s %(num)d',
            {
                'word2': 'baz',
                'num': 1,
                'word1': 'bar'
            }
        )

        logs = log_capture.actual()

        assert (len(logs) == 2)
        assert (('psycopg2', 'INFO', 'foo bar baz 1') == logs.pop(0))
        assert (('psycopg2', 'INFO', 'foo bar baz 1') == logs.pop(0))

    def test_log_custom_logger(self, log_capture):
        log('foo', logger='test')

        logs = log_capture.actual()

        assert (len(logs) == 1)
        assert (('test', 'INFO', 'foo') == logs.pop())
