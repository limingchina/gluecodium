

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
#include "another/SomeCoolClassType.h"

using SomeCoolClassType = ::another::SomeCoolClassType;



void register_another_SomeCoolClassType(py::module_& module) {
auto cls_SomeCoolClassType = py::class_<SomeCoolClassType, std::shared_ptr<SomeCoolClassType>>(module, "another_SomeCoolClassType")
        .def("__gluecodium_id__", [](const SomeCoolClassType& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def("do_important_stuff", &SomeCoolClassType::do_important_stuff)
        ;


}
