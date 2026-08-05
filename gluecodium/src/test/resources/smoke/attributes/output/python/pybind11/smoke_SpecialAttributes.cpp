

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
#include "smoke/SpecialAttributes.h"

using SpecialAttributes = ::smoke::SpecialAttributes;



void register_smoke_SpecialAttributes(py::module_& module) {
auto cls_SpecialAttributes = py::class_<SpecialAttributes, std::shared_ptr<SpecialAttributes>>(module, "smoke_SpecialAttributes")
        .def("__gluecodium_id__", [](const SpecialAttributes& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def("with_escaping", &SpecialAttributes::with_escaping)
        .def("with_line_break", &SpecialAttributes::with_line_break)
        ;


}
