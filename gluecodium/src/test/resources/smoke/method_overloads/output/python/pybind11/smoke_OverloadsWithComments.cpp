

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/OverloadsWithComments.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using OverloadsWithComments = ::smoke::OverloadsWithComments;


void register_smoke_OverloadsWithComments(py::module_& module) {
    py::class_<OverloadsWithComments, std::shared_ptr<OverloadsWithComments>>(module, "smoke_OverloadsWithComments")
        .def("do_stuff", py::overload_cast<>(&OverloadsWithComments::do_stuff))
        .def("do_stuff", py::overload_cast<const ::std::string&>(&OverloadsWithComments::do_stuff), py::arg("stuff"))
        ;
}

