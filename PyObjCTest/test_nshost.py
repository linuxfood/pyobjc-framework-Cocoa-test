import Foundation
from PyObjCTest.testhelper import PyObjC_TestClass3
from PyObjCTools.TestSupport import TestCase


class TestNSHost(TestCase):
    def testCreation(self):
        #
        # This gives an exception on GNUstep:
        #   Foundation.NSRecursiveLockException - unlock: failed to unlock mutex
        #
        # testIndirectCreation performs the same operation from Objective-C
        # and doesn't fail. I don't see any significant differences in the
        # implementation of -hostWithAddress: and -hostWithName: yet the latter
        # does not have the problem we're seeing here.
        #
        o = Foundation.NSHost.hostWithAddress_(b"127.0.0.1".decode("ascii"))
        self.assertEqual(o.addresses(), (b"127.0.0.1".decode("ascii"),))
        self.assertEqual(o.address(), b"127.0.0.1".decode("ascii"))

    def testCreation2(self):
        o = Foundation.NSHost.hostWithName_(b"localhost".decode("ascii"))
        lst = sorted(o.addresses())
        self.assertIn(
            lst,
            (
                [b"127.0.0.1".decode("ascii"), b"::1".decode("ascii")],
                [b"127.0.0.1".decode("ascii")],
            ),
        )
        self.assertEqual(o.address(), o.addresses()[0])

    def testIndirectCreation(self):
        o = PyObjC_TestClass3.createAHostWithAddress_(b"127.0.0.1".decode("ascii"))
        self.assertEqual(o.address(), b"127.0.0.1".decode("ascii"))

    def testMethods(self):
        self.assertArgIsBOOL(Foundation.NSHost.setHostCacheEnabled_, 0)
        self.assertResultIsBOOL(Foundation.NSHost.isHostCacheEnabled)
        self.assertResultIsBOOL(Foundation.NSHost.isEqualToHost_)
