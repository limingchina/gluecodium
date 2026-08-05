

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
#include "smoke/LambdasDeclarationOrder.h"
#include "smoke/LambdasInterface.h"
#include "smoke/LambdasWithStructuredTypes.h"
#include "functional"
#include "memory"

using LambdasWithStructuredTypes = ::smoke::LambdasWithStructuredTypes;



void register_smoke_LambdasWithStructuredTypes(py::module_& module) {
auto cls_LambdasWithStructuredTypes = py::class_<LambdasWithStructuredTypes, std::shared_ptr<LambdasWithStructuredTypes>>(module, "smoke_LambdasWithStructuredTypes")
        .def("__gluecodium_id__", [](const LambdasWithStructuredTypes& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
                .def("do_class_stuff", [](LambdasWithStructuredTypes& self, const ::std::function<void(const ::std::shared_ptr< ::smoke::LambdasInterface >&)>& callback) {
                        self.do_class_stuff(callback);
                }, py::arg("callback"))
                .def("do_struct_stuff", [](LambdasWithStructuredTypes& self, const ::std::function<void(const ::smoke::LambdasDeclarationOrder::SomeStruct&)>& callback) {
                        self.do_struct_stuff(callback);
                }, py::arg("callback"))
        ;


}
