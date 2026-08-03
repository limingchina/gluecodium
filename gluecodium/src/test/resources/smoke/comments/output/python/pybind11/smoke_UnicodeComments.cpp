

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
#include "smoke/UnicodeComments.h"
#include "string"

using UnicodeComments = ::smoke::UnicodeComments;



void register_smoke_UnicodeComments(py::module_& module) {
auto cls_UnicodeComments = py::class_<UnicodeComments, std::shared_ptr<UnicodeComments>>(module, "smoke_UnicodeComments")
        .def("__gluecodium_id__", [](const UnicodeComments& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def("some_method_with_all_comments", &UnicodeComments::some_method_with_all_comments, py::arg("input"))
        ;


}
