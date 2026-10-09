

#include <Python.h>
#include <pybind11/pybind11.h>
#include "_opaque_types.h"
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"
#include "_locale_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "core/duration.h"
#include "cstdint"




void register_smoke_DurationExternal(py::module_& module) {
auto cls_DurationExternal = py::class_<std::chrono::duration<uint64_t, std::ratio<1,1000>>>(module, "smoke_DurationExternal")
        .def_property_readonly("value", [](const std::chrono::duration<uint64_t, std::ratio<1,1000>>& self) -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.count();
            });
        })
        .def(py::init<uint64_t>(), py::arg("value"))
        ;


}
