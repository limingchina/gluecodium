

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"
#include "_locale_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/MultiLineComments.h"
#include "string"

using MultiLineComments = ::smoke::MultiLineComments;



void register_smoke_MultiLineComments(py::module_& module) {
auto cls_MultiLineComments = py::class_<MultiLineComments, std::shared_ptr<MultiLineComments>>(module, "smoke_MultiLineComments")
        .def("__gluecodium_id__", [](const MultiLineComments& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def("some_method_with_long_comment", &MultiLineComments::some_method_with_long_comment, py::arg("input"), py::arg("ratio"))
        ;


}
