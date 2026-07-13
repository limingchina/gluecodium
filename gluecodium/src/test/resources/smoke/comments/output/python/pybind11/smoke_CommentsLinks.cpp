

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/Comments.h"
#include "smoke/CommentsLinks.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using CommentsLinks = ::smoke::CommentsLinks;

void register_CommentsLinks(py::module_& module) {
    py::class_<CommentsLinks, std::shared_ptr<CommentsLinks>>(module, "CommentsLinks")
        .def("random_method", &CommentsLinks::random_method, py::arg("input_parameter"))
        .def("random_method", &CommentsLinks::random_method, py::arg("text"), py::arg("flag"))
        ;
}

