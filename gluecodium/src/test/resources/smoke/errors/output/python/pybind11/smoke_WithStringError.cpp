

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


void register_smoke_WithStringError(py::module_& module) {
    static py::exception<::std::string> exc(module, "smoke_WithStringError");
    py::register_exception_translator([](std::exception_ptr p) {
        try {
            if (p) std::rethrow_exception(p);
        } catch (const ::std::string& e) {
            const auto message = pybind11::detail::ReturnErrorToString<::std::string>::convert(e);
            PyErr_SetString(exc.ptr(), message.c_str());
        }
    });
    pybind11::detail::registerReturnError<::std::string>(exc.ptr());
}

