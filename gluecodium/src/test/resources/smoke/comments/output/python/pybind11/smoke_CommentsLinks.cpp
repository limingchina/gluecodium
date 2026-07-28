

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
#include "smoke/Comments.h"
#include "smoke/CommentsLinks.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using CommentsLinks = ::smoke::CommentsLinks;


void register_smoke_CommentsLinks(py::module_& module) {
    py::class_<CommentsLinks, std::shared_ptr<CommentsLinks>>(module, "smoke_CommentsLinks")
        .def("__gluecodium_id__", [](const CommentsLinks& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def("random_method", py::overload_cast<const ::smoke::Comments::SomeEnum>(&CommentsLinks::random_method), py::arg("input_parameter"))
        .def("random_method", py::overload_cast<const ::std::string&, const bool>(&CommentsLinks::random_method), py::arg("text"), py::arg("flag"))
        ;
}

