

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/PlatformComments.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using PlatformComments = ::smoke::PlatformComments;

void register_PlatformComments(py::module_& module) {
    py::class_<PlatformComments, std::shared_ptr<PlatformComments>>(module, "PlatformComments")
        .def("do_nothing", &PlatformComments::do_nothing)
        .def("do_magic", &PlatformComments::do_magic)
        .def("some_method_with_all_comments", &PlatformComments::some_method_with_all_comments, py::arg("input"))
        .def("some_deprecated_method", &PlatformComments::some_deprecated_method)
        ;
}

