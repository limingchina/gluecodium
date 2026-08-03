

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
#include "smoke/EnumsInTypeCollection.h"
#include "smoke/EnumsInTypeCollectionInterface.h"

using EnumsInTypeCollectionInterface = ::smoke::EnumsInTypeCollectionInterface;



void register_smoke_EnumsInTypeCollectionInterface(py::module_& module) {
auto cls_EnumsInTypeCollectionInterface = py::class_<EnumsInTypeCollectionInterface, std::shared_ptr<EnumsInTypeCollectionInterface>>(module, "smoke_EnumsInTypeCollectionInterface")
        .def("__gluecodium_id__", [](const EnumsInTypeCollectionInterface& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def_static("flip_enum_value", &EnumsInTypeCollectionInterface::flip_enum_value, py::arg("input"))
        ;


}
