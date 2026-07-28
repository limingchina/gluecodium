

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
#include "smoke/MultipleAttributesJava.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using MultipleAttributesJava = ::smoke::MultipleAttributesJava;


void register_smoke_MultipleAttributesJava(py::module_& module) {
    py::class_<MultipleAttributesJava, std::shared_ptr<MultipleAttributesJava>>(module, "smoke_MultipleAttributesJava")
        .def("__gluecodium_id__", [](const MultipleAttributesJava& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def("no_lists2", &MultipleAttributesJava::no_lists2)
        .def("no_lists3", &MultipleAttributesJava::no_lists3)
        .def("list_first", &MultipleAttributesJava::list_first)
        .def("list_second", &MultipleAttributesJava::list_second)
        .def("two_lists", &MultipleAttributesJava::two_lists)
        ;
}

