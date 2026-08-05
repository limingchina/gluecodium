

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
#include "smoke_off/UnderscorePackage.h"
#include "string"

using UnderscorePackage = ::smoke_off::UnderscorePackage;



void register_smoke_off_UnderscorePackage(py::module_& module) {
auto cls_UnderscorePackage = py::class_<UnderscorePackage, std::shared_ptr<UnderscorePackage>>(module, "smoke_off_UnderscorePackage")
        .def("__gluecodium_id__", [](const UnderscorePackage& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def_static("basic_method", &UnderscorePackage::basic_method, py::arg("input_string"))
        ;


}
