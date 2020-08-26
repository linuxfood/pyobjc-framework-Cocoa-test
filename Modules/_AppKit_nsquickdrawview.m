
#if !defined(__LP64__) && PY_MAJOR_VERSION == 2 && defined(USE_TOOLBOX_OBJECT_GLUE)
/* As of OSX 10.12 pymactoolbox includes a file that
 * is not longer present, therefore inline the
 * declarations we use instead of using the pymactoolbox.h
 * header file.
 */
extern PyObject* GrafObj_New(GrafPtr);
extern int       GrafObj_Convert(PyObject*, GrafPtr*);

static PyObject*
call_NSQuickDrawView_qdport(PyObject* method, PyObject* self, PyObject* arguments)
{
    PyObject*         result;
    struct objc_super super;
    void*             port;

    if (!PyArg_ParseTuple(arguments, "")) {
        return NULL;
    }

    Py_BEGIN_ALLOW_THREADS
        @try {
            PyObjC_InitSuper(&super, PyObjCSelector_GetClass(method),
                             PyObjCObject_GetObject(self));

            port = ((void* (*)(struct objc_super*, SEL))objc_msgSendSuper)(
                &super, PyObjCSelector_GetSelector(method));

        } @catch (NSException* localException) {
            PyObjCErr_FromObjC(localException);
            result = NULL;
            port   = NULL;
        }
    Py_END_ALLOW_THREADS

    if (port == NULL) {
        if (PyErr_Occurred())
            return NULL;
        result = Py_None;
        Py_INCREF(result);
    } else {
        result = GrafObj_New((GrafPtr)port);
    }

    return result;
}

static void
imp_NSQuickDrawView_qdport(void* cif __attribute__((__unused__)), void* resp, void** args,
                           void* callable)
{
    id       self    = *(id*)args[0];
    GrafPtr* pretval = (GrafPtr*)resp;

    PyObject* result;
    PyObject* arglist = NULL;
    PyObject* pyself  = NULL;
    int       cookie  = 0;

    PyGILState_STATE state = PyGILState_Ensure();

    arglist = PyTuple_New(1);
    if (arglist == NULL)
        goto error;

    pyself = PyObjCObject_NewTransient(self, &cookie);
    if (pyself == NULL)
        goto error;
    PyTuple_SetItem(arglist, 0, pyself);
    Py_INCREF(pyself);

    result = PyObject_Call((PyObject*)callable, arglist, NULL);
    Py_DECREF(arglist);
    arglist = NULL;
    PyObjCObject_ReleaseTransient(pyself, cookie);
    pyself = NULL;
    if (result == NULL)
        goto error;

    GrafObj_Convert(result, pretval);
    Py_DECREF(result);

    if (PyErr_Occurred())
        goto error;

    PyGILState_Release(state);
    return;

error:
    Py_XDECREF(arglist);
    if (pyself) {
        PyObjCObject_ReleaseTransient(pyself, cookie);
    }
    *pretval = NULL;
    PyObjCErr_ToObjCWithGILState(&state);
}

#endif

static int
setup_nsquickdrawview(PyObject* m __attribute__((__unused__)))
{
#if !defined(__LP64__) && PY_MAJOR_VERSION == 2 && defined(USE_TOOLBOX_OBJECT_GLUE)
    Class classNSQuickDrawView = objc_lookUpClass("NSQuickDrawView");
    if (classNSQuickDrawView == NULL) {
        return 0;
    }

    if (PyObjC_RegisterMethodMapping(classNSQuickDrawView, @selector(qdport),
                                     call_NSQuickDrawView_qdport,
                                     imp_NSQuickDrawView_qdport)
        < 0) {

        return -1;
    }
#endif

    return 0;
}
