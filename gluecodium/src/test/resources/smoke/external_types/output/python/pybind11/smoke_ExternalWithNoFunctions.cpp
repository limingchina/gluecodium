

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
#include "some/path/Bar.h"




void register_smoke_ExternalWithNoFunctions(py::module_& module) {
auto cls_ExternalWithNoFunctions = py::class_<::some::path::Bar, std::shared_ptr<::some::path::Bar>>(module, "smoke_ExternalWithNoFunctions")
        .def("__gluecodium_id__", [](const ::some::path::Bar& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        ;


}
