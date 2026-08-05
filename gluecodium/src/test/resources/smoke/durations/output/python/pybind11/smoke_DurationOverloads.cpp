

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
#include "gluecodium/DurationHash.h"
#include "smoke/DurationOverloads.h"
#include "chrono"
#include "string"

using DurationOverloads = ::smoke::DurationOverloads;



void register_smoke_DurationOverloads(py::module_& module) {
auto cls_DurationOverloads = py::class_<DurationOverloads, std::shared_ptr<DurationOverloads>>(module, "smoke_DurationOverloads")
        .def("__gluecodium_id__", [](const DurationOverloads& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def("duration_function", py::overload_cast<const ::std::chrono::seconds>(&DurationOverloads::duration_function), py::arg("input"))
        .def("duration_function", py::overload_cast<const ::std::string&>(&DurationOverloads::duration_function), py::arg("input"))
        ;


}
