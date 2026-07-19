

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/UseJavaExternalConst.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using UseJavaExternalConst = ::smoke::UseJavaExternalConst;

void register_UseJavaExternalConst(py::module_& module) {
    py::class_<UseJavaExternalConst>(module, "UseJavaExternalConst")
        .def_readwrite("string_field", &UseJavaExternalConst::string_field)
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("string_field"))
        ;
}

