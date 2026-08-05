

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
#include "gluecodium/VectorHash.h"
#include "smoke/GlobalListTypeDef.h"
#include "smoke/SomeDartStructWithTypedefField.h"
#include "vector"

using SomeDartStructWithTypedefField = ::smoke::SomeDartStructWithTypedefField;



void register_smoke_SomeDartStructWithTypedefField(py::module_& module) {
auto cls_SomeDartStructWithTypedefField = py::class_<SomeDartStructWithTypedefField>(module, "smoke_SomeDartStructWithTypedefField")
        .def_readwrite("some_field", &SomeDartStructWithTypedefField::some_field)
        .def(py::init<>())
        .def(py::init<::std::vector< float >>(), py::arg("some_field"))
        ;


}
