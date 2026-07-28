

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
#include "smoke/MultipleAttributesSwift.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using MultipleAttributesSwift = ::smoke::MultipleAttributesSwift;


void register_smoke_MultipleAttributesSwift(py::module_& module) {
    py::class_<MultipleAttributesSwift, std::shared_ptr<MultipleAttributesSwift>>(module, "smoke_MultipleAttributesSwift")
        .def("__gluecodium_id__", [](const MultipleAttributesSwift& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def("no_lists2", &MultipleAttributesSwift::no_lists2)
        .def("no_lists3", &MultipleAttributesSwift::no_lists3)
        .def("list_first", &MultipleAttributesSwift::list_first)
        .def("list_second", &MultipleAttributesSwift::list_second)
        .def("two_lists", &MultipleAttributesSwift::two_lists)
        ;
}

