

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
#include "smoke/SomeTypeCollection.h"
#include "smoke/UseTcException.h"

using UseTcException = ::smoke::UseTcException;



void register_smoke_UseTcException(py::module_& module) {
auto cls_UseTcException = py::class_<UseTcException, std::shared_ptr<UseTcException>>(module, "smoke_UseTcException")
        .def("__gluecodium_id__", [](const UseTcException& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def("do_nothing", [](UseTcException& self) {
                const auto error = self.do_nothing();
                if (error) {
                    throw error;
                }
        })
        ;


}
