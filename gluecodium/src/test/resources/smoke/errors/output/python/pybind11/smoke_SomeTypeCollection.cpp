

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

using SomeTypeCollection = ::smoke::SomeTypeCollection;
using SomeTypeCollectionError = ::smoke::SomeTypeCollection::SomeTypeCollectionError;



void register_smoke_SomeTypeCollection(py::module_& module) {
auto cls_SomeTypeCollection = py::class_<SomeTypeCollection>(module, "smoke_SomeTypeCollection")
        .def(py::init<>())
        ;

auto cls_SomeTypeCollectionSomeTypeCollectionError = py::enum_<SomeTypeCollectionError>(cls_SomeTypeCollection, "SomeTypeCollectionError")
        .value("ERROR_A", SomeTypeCollectionError::ERROR_A)
        .value("ERROR_B", SomeTypeCollectionError::ERROR_B)
        ;

    static py::exception<::std::error_code> exc_SomeError(cls_SomeTypeCollection, "SomeError");
    py::register_exception_translator([](std::exception_ptr p) {
        try {
            if (p) std::rethrow_exception(p);
        } catch (const ::std::error_code& e) {
            PyErr_SetString(exc_SomeError.ptr(), e.message().c_str());
        }
    });
    pybind11::detail::registerReturnError<::std::error_code>(exc_SomeError.ptr());


}
