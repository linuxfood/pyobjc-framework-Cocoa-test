import CoreFoundation
import objc
from PyObjCTools.TestSupport import TestCase


class TestCFBag(TestCase):
    def testCreation(self):
        bag = CoreFoundation.CFBagCreate(None, [1, 1, 2, 3, 4], 5)
        self.assertIsInstance(bag, CoreFoundation.CFBagRef)
        self.assertEqual(CoreFoundation.CFBagGetCountOfValue(bag, 1), 2)
        self.assertEqual(CoreFoundation.CFBagGetCountOfValue(bag, 3), 1)

        bag = CoreFoundation.CFBagCreateMutable(None, 0)
        self.assertIsInstance(bag, CoreFoundation.CFBagRef)
        CoreFoundation.CFBagAddValue(bag, 9)
        CoreFoundation.CFBagAddValue(bag, 8)
        CoreFoundation.CFBagAddValue(bag, 9)
        self.assertEqual(CoreFoundation.CFBagGetCountOfValue(bag, 9), 2)
        self.assertEqual(CoreFoundation.CFBagGetCountOfValue(bag, 8), 1)

    def testApplyFunction(self):
        items = []
        contexts = []

        bag = CoreFoundation.CFBagCreate(None, [1, 1, 2, 3, 4], 5)

        def func(item, context):
            items.append(item * item)
            contexts.append(context)

        CoreFoundation.CFBagApplyFunction(bag, func, 99)
        items.sort()
        self.assertEqual(items, [1, 1, 4, 9, 16])
        self.assertEqual(contexts, [99, 99, 99, 99, 99])

    def testTypeID(self):
        v = CoreFoundation.CFBagGetTypeID()
        self.assertIsInstance(v, int)

    def testCopy(self):
        bag = CoreFoundation.CFBagCreate(None, [1, 1, 2, 3, 4], 5)
        self.assertIsInstance(bag, CoreFoundation.CFBagRef)
        bag2 = CoreFoundation.CFBagCreateCopy(None, bag)
        self.assertIsInstance(bag2, CoreFoundation.CFBagRef)
        bag3 = CoreFoundation.CFBagCreateMutableCopy(None, 0, bag)
        self.assertIsInstance(bag3, CoreFoundation.CFBagRef)
        self.assertIsNot(bag3, bag)

    def testInspect(self):
        bag = CoreFoundation.CFBagCreate(
            None,
            [
                b"Hello".decode("ascii"),
                42,
                b"World".decode("ascii"),
                42,
                b"a".decode("ascii"),
                b"a".decode("ascii"),
                b"a".decode("ascii"),
            ],
            7,
        )
        self.assertIsInstance(bag, CoreFoundation.CFBagRef)
        self.assertEqual(CoreFoundation.CFBagGetCount(bag), 7)
        self.assertEqual(
            CoreFoundation.CFBagGetCountOfValue(bag, b"Hello".decode("ascii")), 1
        )
        self.assertEqual(CoreFoundation.CFBagGetCountOfValue(bag, 42), 2)
        self.assertEqual(
            CoreFoundation.CFBagGetCountOfValue(bag, b"a".decode("ascii")), 3
        )
        self.assertTrue(CoreFoundation.CFBagContainsValue(bag, b"a".decode("ascii")))
        self.assertFalse(CoreFoundation.CFBagContainsValue(bag, b"b".decode("ascii")))

        v = CoreFoundation.CFBagGetValue(bag, b"b".decode("ascii"))
        self.assertIs(v, None)
        v = CoreFoundation.CFBagGetValue(bag, b"a".decode("ascii"))
        self.assertEqual(v, b"a".decode("ascii"))
        exists, value = CoreFoundation.CFBagGetValueIfPresent(
            bag, b"a".decode("ascii"), None
        )
        self.assertTrue(exists)
        self.assertEqual(value, b"a".decode("ascii"))
        exists, value = CoreFoundation.CFBagGetValueIfPresent(
            bag, b"b".decode("ascii"), None
        )
        self.assertFalse(exists)
        self.assertIs(value, None)
        values = set(CoreFoundation.CFBagGetValues(bag))
        expected = {
            b"Hello".decode("ascii"),
            42,
            b"World".decode("ascii"),
            42,
            b"a".decode("ascii"),
            b"a".decode("ascii"),
            b"a".decode("ascii"),
        }
        self.assertEqual(values, expected)

    def testMutation(self):
        bag = CoreFoundation.CFBagCreateMutable(None, 0)
        self.assertEqual(CoreFoundation.CFBagGetCount(bag), 0)
        CoreFoundation.CFBagAddValue(bag, b"hello".decode("ascii"))
        self.assertEqual(CoreFoundation.CFBagGetCount(bag), 1)
        CoreFoundation.CFBagAddValue(bag, b"hello".decode("ascii"))
        self.assertEqual(CoreFoundation.CFBagGetCount(bag), 2)
        CoreFoundation.CFBagReplaceValue(bag, b"hello".decode("ascii"))
        self.assertEqual(CoreFoundation.CFBagGetCount(bag), 2)
        CoreFoundation.CFBagReplaceValue(bag, b"world".decode("ascii"))
        self.assertEqual(CoreFoundation.CFBagGetCount(bag), 2)
        CoreFoundation.CFBagSetValue(bag, b"world".decode("ascii"))
        self.assertEqual(CoreFoundation.CFBagGetCount(bag), 3)
        CoreFoundation.CFBagSetValue(bag, b"world".decode("ascii"))
        self.assertEqual(CoreFoundation.CFBagGetCount(bag), 3)
        CoreFoundation.CFBagRemoveValue(bag, b"hello".decode("ascii"))
        self.assertEqual(CoreFoundation.CFBagGetCount(bag), 2)
        CoreFoundation.CFBagRemoveValue(bag, b"hello".decode("ascii"))
        self.assertEqual(CoreFoundation.CFBagGetCount(bag), 1)
        CoreFoundation.CFBagRemoveAllValues(bag)
        self.assertEqual(CoreFoundation.CFBagGetCount(bag), 0)

    def testFunctions(self):
        self.assertArgHasType(CoreFoundation.CFBagGetCountOfValue, 1, b"@")
        self.assertArgHasType(CoreFoundation.CFBagContainsValue, 1, b"@")
        self.assertArgHasType(CoreFoundation.CFBagGetValue, 1, b"@")
        self.assertResultHasType(CoreFoundation.CFBagGetValue, b"@")
        self.assertArgHasType(CoreFoundation.CFBagGetValueIfPresent, 1, b"@")
        self.assertArgHasType(CoreFoundation.CFBagGetValueIfPresent, 2, b"o^@")
        self.assertResultHasType(CoreFoundation.CFBagGetValueIfPresent, objc._C_NSBOOL)
        self.assertArgIsFunction(CoreFoundation.CFBagApplyFunction, 1, b"v@@", False)
        self.assertArgHasType(CoreFoundation.CFBagApplyFunction, 2, b"@")
        self.assertArgHasType(CoreFoundation.CFBagAddValue, 1, b"@")
        self.assertArgHasType(CoreFoundation.CFBagReplaceValue, 1, b"@")
        self.assertArgHasType(CoreFoundation.CFBagSetValue, 1, b"@")
        self.assertArgHasType(CoreFoundation.CFBagRemoveValue, 1, b"@")
